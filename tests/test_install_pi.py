from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install-pi.py"
SPEC = importlib.util.spec_from_file_location("install_pi", SCRIPT_PATH)
assert SPEC and SPEC.loader
install_pi = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = install_pi
SPEC.loader.exec_module(install_pi)


class TargetSelectionTest(unittest.TestCase):
    def test_manages_pi_by_default_or_when_explicitly_requested(self) -> None:
        self.assertTrue(install_pi.should_manage_pi(None, None))
        self.assertTrue(install_pi.should_manage_pi("pi,codex", None))

    def test_skips_pi_for_other_agents_or_explicit_skill_destination(self) -> None:
        self.assertFalse(install_pi.should_manage_pi("codex", None))
        self.assertFalse(install_pi.should_manage_pi(None, "/tmp/skills"))


class PinnedVersionTest(unittest.TestCase):
    def test_reads_pi_version_from_package_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "pi-packages.json").write_text(
                json.dumps({"piVersion": "0.84.2", "packages": []}),
                encoding="utf-8",
            )
            with patch.object(install_pi, "repo_root", return_value=root):
                version = install_pi.load_pinned_version()

        self.assertEqual(version, "0.84.2")


class MidturnCompactionPatchTest(unittest.TestCase):
    SDK_FIXTURE = '''import { formatNoModelsAvailableMessage } from "./auth-guidance.js";
import { DEFAULT_THINKING_LEVEL } from "./defaults.js";
import { convertToLlm } from "./messages.js";
import { getDefaultSessionDir, SessionManager } from "./session-manager.js";
    agent = new Agent({
        maxRetryDelayMs: settingsManager.getProviderRetrySettings().maxRetryDelayMs,
    });
    // Restore messages if session has existing data
'''

    SESSION_FIXTURE = '''    _overflowRecoveryAttempted = false;
    // Branch summarization state
        // Emit to extensions first
        await this._emitExtensionEvent(event);
        // Case 2: Threshold - context is getting large
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

    def make_package(self, root: Path) -> None:
        (root / "dist" / "core").mkdir(parents=True)
        (root / "package.json").write_text(
            json.dumps({"name": install_pi.PI_PACKAGE, "version": "0.84.2"}),
            encoding="utf-8",
        )
        (root / "dist" / "core" / "sdk.js").write_text(self.SDK_FIXTURE, encoding="utf-8")
        (root / "dist" / "core" / "agent-session.js").write_text(
            self.SESSION_FIXTURE,
            encoding="utf-8",
        )

    def test_applies_midturn_guard_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_package(root)

            first = install_pi.patch_pi_midturn_compaction(root, "0.84.2", dry_run=False)
            second = install_pi.patch_pi_midturn_compaction(root, "0.84.2", dry_run=False)
            sdk = (root / "dist" / "core" / "sdk.js").read_text(encoding="utf-8")
            session = (root / "dist" / "core" / "agent-session.js").read_text(encoding="utf-8")

        self.assertTrue(first)
        self.assertFalse(second)
        self.assertIn("agent.shouldStopAfterTurn", sdk)
        self.assertIn("shouldCompactMessages(context.messages)", sdk)
        self.assertIn("if (estimate.lastUsageIndex !== null)", sdk)
        self.assertIn("shouldResumeToolLoop", session)
        self.assertIn("estimate.lastUsageIndex === null ? estimate.tokens", session)
        self.assertIn("_lastToolBatchTerminated", session)
        self.assertIn('event.type === "tool_execution_end"', session)
        self.assertIn("event.result.terminate === true", session)
        self.assertIn('._runAutoCompaction("threshold", shouldResumeToolLoop)', session)
        self.assertIn("contextTokens < contextWindow - emergencyReserve", session)

    def test_repairs_a_reviewed_partial_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_package(root)
            install_pi.patch_pi_midturn_compaction(root, "0.84.2", dry_run=False)
            session_path = root / "dist" / "core" / "agent-session.js"
            session_path.write_text(self.SESSION_FIXTURE, encoding="utf-8")

            changed = install_pi.patch_pi_midturn_compaction(root, "0.84.2", dry_run=False)
            session = session_path.read_text(encoding="utf-8")

        self.assertTrue(changed)
        self.assertIn("shouldResumeToolLoop", session)

    def test_rejects_a_corrupted_partial_patch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_package(root)
            sdk_path = root / "dist" / "core" / "sdk.js"
            sdk_path.write_text(
                sdk_path.read_text(encoding="utf-8") + "// Mid-turn compaction guard:\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "incomplete or corrupted"):
                install_pi.patch_pi_midturn_compaction(root, "0.84.2", dry_run=False)

    def test_rejects_patch_for_unreviewed_pi_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_package(root)
            with self.assertRaisesRegex(ValueError, "only reviewed for Pi 0.84.2"):
                install_pi.patch_pi_midturn_compaction(root, "0.85.0", dry_run=False)


class EnsurePiTest(unittest.TestCase):
    def test_keeps_matching_pi_without_invoking_npm(self) -> None:
        with (
            patch.object(install_pi.shutil, "which", return_value="/usr/local/bin/pi"),
            patch.object(install_pi, "get_pi_version", return_value="0.84.2"),
            patch.object(install_pi, "ensure_midturn_compaction_patch") as patch_guard,
            patch.object(install_pi.subprocess, "run") as run,
            redirect_stdout(io.StringIO()),
        ):
            result = install_pi.ensure_pi("0.84.2", dry_run=False)

        self.assertEqual(result, 0)
        patch_guard.assert_called_once_with("/usr/local/bin/pi", "0.84.2", False)
        run.assert_not_called()

    def test_dry_run_reports_install_when_pi_is_missing(self) -> None:
        def which(name: str) -> str | None:
            return "/usr/local/bin/npm" if name == "npm" else None

        output = io.StringIO()
        with (
            patch.object(install_pi.shutil, "which", side_effect=which),
            patch.object(install_pi.subprocess, "run") as run,
            redirect_stdout(output),
        ):
            result = install_pi.ensure_pi("0.84.2", dry_run=True)

        self.assertEqual(result, 0)
        run.assert_not_called()
        self.assertIn("@earendil-works/pi-coding-agent@0.84.2", output.getvalue())

    def test_reconciles_a_different_pi_version_with_npm(self) -> None:
        def which(name: str) -> str | None:
            return f"/usr/local/bin/{name}" if name in {"pi", "npm"} else None

        with (
            patch.object(install_pi.shutil, "which", side_effect=which),
            patch.object(install_pi, "get_pi_version", side_effect=["0.80.0", "0.84.2"]),
            patch.object(install_pi, "ensure_midturn_compaction_patch") as patch_guard,
            patch.object(install_pi.subprocess, "run") as run,
            redirect_stdout(io.StringIO()),
        ):
            result = install_pi.ensure_pi("0.84.2", dry_run=False)

        self.assertEqual(result, 0)
        patch_guard.assert_called_once_with("/usr/local/bin/pi", "0.84.2", dry_run=False)
        run.assert_called_once_with(
            [
                "/usr/local/bin/npm",
                "install",
                "--global",
                "--ignore-scripts",
                "@earendil-works/pi-coding-agent@0.84.2",
            ],
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
