#!/usr/bin/env python3
"""Install the repository-pinned Pi CLI version when Pi is targeted."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PI_PACKAGE = "@earendil-works/pi-coding-agent"
MIDTURN_PATCH_VERSION = "0.84.2"
VERSION_PATTERN = re.compile(r"(?<!\d)(\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)(?!\d)")

SDK_GUARD_ANCHOR = '''        maxRetryDelayMs: settingsManager.getProviderRetrySettings().maxRetryDelayMs,
    });
    // Restore messages if session has existing data
'''
SDK_GUARD_REPLACEMENT = '''        maxRetryDelayMs: settingsManager.getProviderRetrySettings().maxRetryDelayMs,
    });
    // Mid-turn compaction guard: stop after a complete tool batch before the next provider request.
    const shouldCompactMessages = (messages) => {
        const compactionSettings = settingsManager.getCompactionSettings();
        if (!compactionSettings.enabled)
            return false;
        const contextWindow = agent.state.model?.contextWindow ?? 0;
        if (contextWindow === 0)
            return false;
        const estimate = estimateContextTokens(messages);
        if (estimate.lastUsageIndex !== null) {
            const compactionEntry = getLatestCompactionEntry(sessionManager.getBranch());
            if (compactionEntry) {
                const usageMessage = messages[estimate.lastUsageIndex];
                if (usageMessage.role === "assistant" &&
                    usageMessage.timestamp <= new Date(compactionEntry.timestamp).getTime()) {
                    return false;
                }
            }
        }
        return shouldCompact(estimate.tokens, contextWindow, compactionSettings);
    };
    agent.shouldStopAfterTurn = ({ message, context }) => {
        if (message.stopReason === "error" || message.stopReason === "aborted")
            return false;
        return shouldCompactMessages(context.messages);
    };
    // Restore messages if session has existing data
'''

SESSION_TERMINATION_FIELDS_ANCHOR = '''    _overflowRecoveryAttempted = false;
    // Branch summarization state
'''
SESSION_TERMINATION_FIELDS_REPLACEMENT = '''    _overflowRecoveryAttempted = false;
    // Track whether every result in the latest tool batch intentionally terminates the loop.
    _terminatingToolCallIds = new Set();
    _lastToolBatchTerminated = false;
    // Branch summarization state
'''
SESSION_TURN_END_ANCHOR = '''        // Emit to extensions first
        await this._emitExtensionEvent(event);
'''
SESSION_TURN_END_REPLACEMENT = '''        if (event.type === "tool_execution_end") {
            if (event.result.terminate === true) {
                this._terminatingToolCallIds.add(event.toolCallId);
            }
            else {
                this._terminatingToolCallIds.delete(event.toolCallId);
            }
        }
        if (event.type === "turn_end") {
            this._lastToolBatchTerminated = event.toolResults.length > 0 &&
                event.toolResults.every((result) => this._terminatingToolCallIds.has(result.toolCallId));
            for (const result of event.toolResults) {
                this._terminatingToolCallIds.delete(result.toolCallId);
            }
        }
        // Emit to extensions first
        await this._emitExtensionEvent(event);
'''

SESSION_THRESHOLD_ANCHOR = '''        // Case 2: Threshold - context is getting large
        // For error messages or all-zero usage messages, estimate from the last valid response.
        // This ensures sessions that hit persistent API errors (e.g. 529) or malformed zero-usage
        // responses can still compact and do not reset context accounting.
        let contextTokens;
        const directContextTokens = assistantMessage.usage ? calculateContextTokens(assistantMessage.usage) : 0;
        if (assistantMessage.stopReason === "error" || directContextTokens === 0) {
            const messages = this.agent.state.messages;
            const estimate = estimateContextTokens(messages);
            if (estimate.lastUsageIndex === null)
                return false; // No usage data at all
            // Verify the usage source is post-compaction. Kept pre-compaction messages
            // have stale usage reflecting the old (larger) context and would falsely
            // trigger compaction right after one just finished.
            const usageMsg = messages[estimate.lastUsageIndex];
            if (compactionEntry &&
                usageMsg.role === "assistant" &&
                usageMsg.timestamp <= new Date(compactionEntry.timestamp).getTime()) {
                return false;
            }
            contextTokens = estimate.tokens;
        }
        else {
            contextTokens = directContextTokens;
        }
        if (shouldCompact(contextTokens, contextWindow, settings)) {
            return await this._runAutoCompaction("threshold", false);
        }
        return false;
'''
SDK_PATCH_SENTINELS = (
    "// Mid-turn compaction guard:",
    "agent.shouldStopAfterTurn",
    "getLatestCompactionEntry, SessionManager",
    "shouldCompactMessages(context.messages)",
)
SESSION_PATCH_SENTINELS = (
    "_terminatingToolCallIds = new Set()",
    "event.result.terminate === true",
    "event.toolResults.every((result) => this._terminatingToolCallIds.has(result.toolCallId))",
    "// Case 2: Threshold - include tool results appended after the last provider usage.",
    "!this._lastToolBatchTerminated",
    '._runAutoCompaction("threshold", shouldResumeToolLoop)',
    "contextTokens < contextWindow - emergencyReserve",
)

SESSION_THRESHOLD_REPLACEMENT = '''        // Case 2: Threshold - include tool results appended after the last provider usage.
        const messages = this.agent.state.messages;
        const estimate = estimateContextTokens(messages);
        let estimatedContextTokens = estimate.lastUsageIndex === null ? estimate.tokens : undefined;
        if (estimate.lastUsageIndex !== null) {
            const usageMsg = messages[estimate.lastUsageIndex];
            const usageIsFromBeforeCompaction = compactionEntry &&
                usageMsg.role === "assistant" &&
                usageMsg.timestamp <= new Date(compactionEntry.timestamp).getTime();
            if (!usageIsFromBeforeCompaction) {
                estimatedContextTokens = estimate.tokens;
            }
        }
        const directContextTokens = assistantMessage.usage ? calculateContextTokens(assistantMessage.usage) : 0;
        let contextTokens;
        if (assistantMessage.stopReason === "error" || directContextTokens === 0) {
            if (estimatedContextTokens === undefined)
                return false;
            contextTokens = estimatedContextTokens;
        }
        else {
            contextTokens = Math.max(directContextTokens, estimatedContextTokens ?? 0);
        }
        if (shouldCompact(contextTokens, contextWindow, settings)) {
            const lastMessage = messages[messages.length - 1];
            const shouldResumeToolLoop = assistantMessage.stopReason !== "error" &&
                lastMessage?.role !== "assistant" &&
                !this._lastToolBatchTerminated;
            this._lastToolBatchTerminated = false;
            const compactionContinues = await this._runAutoCompaction("threshold", shouldResumeToolLoop);
            if (compactionContinues || !shouldResumeToolLoop) {
                return compactionContinues;
            }
            // A transient compaction failure must not strand a safe interrupted tool loop.
            // Resume only while enough hard-window headroom remains to attempt compaction again.
            const emergencyReserve = Math.min(16000, Math.floor(contextWindow * 0.1));
            return contextTokens < contextWindow - emergencyReserve;
        }
        return false;
'''


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def should_manage_pi(agent: str | None, dest: str | None) -> bool:
    if dest:
        return False
    requested = {name.strip() for name in (agent or "").split(",") if name.strip()}
    return not requested or "pi" in requested


def load_pinned_version() -> str:
    manifest_path = repo_root() / "pi-packages.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Missing Pi package manifest: {manifest_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {manifest_path}: {error}") from error

    version = str(manifest.get("piVersion", "")).strip()
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError("pi-packages.json must contain a valid piVersion")
    return version


def get_pi_version(pi: str) -> str | None:
    result = subprocess.run(
        [pi, "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    match = VERSION_PATTERN.search(f"{result.stdout}\n{result.stderr}")
    return match.group(1) if result.returncode == 0 and match else None


def find_pi_package_root(pi: str) -> Path:
    resolved = Path(pi).resolve()
    for candidate in resolved.parents:
        package_path = candidate / "package.json"
        if not package_path.is_file():
            continue
        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if package.get("name") == PI_PACKAGE:
            return candidate
    raise ValueError(f"Could not locate {PI_PACKAGE} from {pi}")


def _replace_once(source: str, old: str, new: str, path: Path) -> str:
    count = source.count(old)
    if count != 1:
        raise ValueError(f"Expected one reviewed patch anchor in {path}; found {count}")
    return source.replace(old, new)


def _patch_state(source: str, sentinels: tuple[str, ...], path: Path) -> bool:
    matches = [sentinel in source for sentinel in sentinels]
    if any(matches) and not all(matches):
        raise ValueError(f"Pi mid-turn compaction patch is incomplete or corrupted in {path}")
    return all(matches)


def _stage_write(path: Path, content: str) -> Path:
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
        os.chmod(temp_path, path.stat().st_mode)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise
    return temp_path


def patch_pi_midturn_compaction(package_root: Path, version: str, dry_run: bool) -> bool:
    if version != MIDTURN_PATCH_VERSION:
        raise ValueError(f"Mid-turn compaction patch is only reviewed for Pi {MIDTURN_PATCH_VERSION}")

    package_path = package_root / "package.json"
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read Pi package metadata: {package_path}") from error
    if package.get("name") != PI_PACKAGE or package.get("version") != version:
        raise ValueError(f"Unexpected Pi package at {package_root}")

    sdk_path = package_root / "dist" / "core" / "sdk.js"
    session_path = package_root / "dist" / "core" / "agent-session.js"
    sdk_source = sdk_path.read_text(encoding="utf-8")
    session_source = session_path.read_text(encoding="utf-8")
    sdk_patched = _patch_state(sdk_source, SDK_PATCH_SENTINELS, sdk_path)
    session_patched = _patch_state(session_source, SESSION_PATCH_SENTINELS, session_path)
    if sdk_patched and session_patched:
        return False

    outputs: list[tuple[Path, str]] = []
    if not sdk_patched:
        sdk_source = _replace_once(
            sdk_source,
            'import { formatNoModelsAvailableMessage } from "./auth-guidance.js";\n',
            'import { formatNoModelsAvailableMessage } from "./auth-guidance.js";\n'
            'import { estimateContextTokens, shouldCompact } from "./compaction/index.js";\n',
            sdk_path,
        )
        sdk_source = _replace_once(
            sdk_source,
            'import { getDefaultSessionDir, SessionManager } from "./session-manager.js";\n',
            'import { getDefaultSessionDir, getLatestCompactionEntry, SessionManager } from "./session-manager.js";\n',
            sdk_path,
        )
        sdk_source = _replace_once(sdk_source, SDK_GUARD_ANCHOR, SDK_GUARD_REPLACEMENT, sdk_path)
        _patch_state(sdk_source, SDK_PATCH_SENTINELS, sdk_path)
        outputs.append((sdk_path, sdk_source))
    if not session_patched:
        for old, new in (
            (SESSION_TERMINATION_FIELDS_ANCHOR, SESSION_TERMINATION_FIELDS_REPLACEMENT),
            (SESSION_TURN_END_ANCHOR, SESSION_TURN_END_REPLACEMENT),
            (SESSION_THRESHOLD_ANCHOR, SESSION_THRESHOLD_REPLACEMENT),
        ):
            session_source = _replace_once(session_source, old, new, session_path)
        _patch_state(session_source, SESSION_PATCH_SENTINELS, session_path)
        outputs.append((session_path, session_source))

    if dry_run:
        return True

    staged: list[tuple[Path, Path]] = []
    try:
        for path, content in outputs:
            staged.append((path, _stage_write(path, content)))
        for path, temp_path in staged:
            os.replace(temp_path, path)
    finally:
        for _path, temp_path in staged:
            temp_path.unlink(missing_ok=True)
    return True


def ensure_midturn_compaction_patch(pi: str, version: str, dry_run: bool) -> None:
    package_root = find_pi_package_root(pi)
    changed = patch_pi_midturn_compaction(package_root, version, dry_run)
    if changed:
        prefix = "[DRY]" if dry_run else "[PATCH]"
        print(f"{prefix} Enable safe mid-turn native compaction for Pi {version}")
    else:
        print(f"[OK] Pi {version} mid-turn compaction guard is installed")


def ensure_pi(version: str, dry_run: bool) -> int:
    pi = shutil.which("pi")
    current_version = get_pi_version(pi) if pi else None
    if current_version == version:
        try:
            ensure_midturn_compaction_patch(pi, version, dry_run)
        except (OSError, ValueError) as error:
            print(error, file=sys.stderr)
            return 1
        print(f"[OK] Pi CLI {version} is installed")
        return 0

    npm = shutil.which("npm")
    if not npm:
        print(
            "npm is required to install Pi. Install Node.js 22.19 or newer and retry.",
            file=sys.stderr,
        )
        return 1

    package_spec = f"{PI_PACKAGE}@{version}"
    if dry_run:
        action = "install" if current_version is None else f"replace Pi {current_version} with"
        print(
            f"[DRY] npm install --global --ignore-scripts {package_spec} "
            f"({action} {version})"
        )
        return 0

    if current_version is None:
        print(f"[INSTALL] Pi CLI {version}")
    else:
        print(f"[INSTALL] Reconcile Pi CLI {current_version} -> {version}")
    subprocess.run(
        [npm, "install", "--global", "--ignore-scripts", package_spec],
        check=True,
    )

    installed_pi = shutil.which("pi")
    installed_version = get_pi_version(installed_pi) if installed_pi else None
    if installed_version != version:
        print(
            f"Pi installation did not produce expected version {version}; found {installed_version or 'none'}",
            file=sys.stderr,
        )
        return 1
    try:
        ensure_midturn_compaction_patch(installed_pi, version, dry_run=False)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"[OK] Pi CLI {version} installed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install the repository-pinned Pi CLI version.",
        add_help=True,
    )
    parser.add_argument("--agent", help="Comma-separated harness targets from bootstrap.sh")
    parser.add_argument("--dest", help="Explicit skill destination; skips Pi installation")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list", action="store_true")
    args, _unknown = parser.parse_known_args()

    if not should_manage_pi(args.agent, args.dest):
        print("[SKIP] Pi CLI was not requested")
        return 0

    try:
        version = load_pinned_version()
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if args.list:
        print(f"pi\tnpm:{PI_PACKAGE}@{version}")
        return 0
    return ensure_pi(version, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
