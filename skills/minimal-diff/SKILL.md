---
name: minimal-diff
description: Audit whether a code change is the smallest correct, reviewable, and reversible diff. Use when a patch is expanding beyond its stated scope, when the user asks to minimize or review a diff, or before handing off a risky or broad change. Do not invoke automatically for every trivial edit.
license: Apache-2.0
---

# Minimal Diff

Make the smallest correct change that satisfies the request. Optimize for reviewer cognitive load and limited blast radius, not merely the fewest changed lines.

Invoke this skill intentionally as a scope-control or final-diff audit. Repository instructions should already prevent drive-by edits during ordinary work; this skill adds explicit diff sizing and reversibility checks when those risks are material.

## Workflow

### 1. Set the diff envelope

Before editing, state briefly:

- **Intent:** the requested behavior or outcome.
- **In scope:** files, modules, public surfaces, and tests expected to change.
- **Out of scope:** nearby cleanup or improvements not required for correctness.
- **Forbidden zones:** generated/vendor files, migrations, dependencies, configuration, or public APIs that should not change without approval.
- **Acceptance signal:** the test, reproduction, build, or benchmark that proves success.

Keep this inline in the working plan or task update; do not create an audit file unless the repository requires one.

### 2. Make the narrowest correct change

- Follow the existing design and style instead of introducing a new abstraction for one use.
- Include every change required for correctness, including focused tests and cleanup made necessary by your own edit.
- Prefer changing a call site over widening a shared interface when both solve the problem correctly.
- Do not under-fix merely to reduce line count.
- Do not alter unrelated user changes already present in the worktree.

### 3. Block drive-by edits

Do not include unrelated:

- formatting, import sorting, quote or indentation normalization;
- renames, comment rewrites, type tightening, or deprecated-API cleanup;
- logging, dependency updates, config changes, or test cleanup;
- refactors justified only by “while I’m here.”

If an apparently unrelated change is required for the requested behavior to build or work, explain why and expand the scope explicitly. Otherwise revert it and optionally mention it as a follow-up suggestion.

### 4. Inspect diff size and shape

Use repository-aware commands such as:

```bash
git status --short
git diff --stat
git diff --numstat
git diff --check
git diff -- <touched-paths>
```

Review every changed hunk. Compare it with the diff envelope and remove anything that cannot be traced to the request.

Treat these as prompts to pause, not rigid quality metrics:

| Task | Pause and reassess around |
| --- | --- |
| Small bug fix | 100 changed lines or 4 files |
| Small feature | 200 changed lines or 6 files |
| Behavior-preserving refactor | 400 changed lines or 10 files |
| Mechanical migration | Use an explicit file list and separate validation |

If the change is materially larger than expected, first seek a narrower implementation. If none exists, explain the scope expansion and ask before crossing a risky boundary.

### 5. Verify correctness and reversibility

- Run the narrowest relevant test first, then the repository’s broader required checks.
- Confirm `git diff --check` passes.
- Ensure reverting only this change would restore prior code behavior without requiring unrelated code edits.
- For persistent side effects such as schema changes, data writes, cache mutations, or external calls, provide a rollback plan and get approval before proceeding.
- Prefer additive, expand-and-contract steps when a one-step rollback is unsafe.

Do not run destructive revert commands merely to prove reversibility in a dirty worktree.

### 6. Separate concerns when needed

If the work necessarily contains distinct concerns—such as a mechanical rename, a prerequisite refactor, the behavior change, and tests—keep their hunks separable. When the user asks for commits, split them in dependency order and follow the repository’s commit style.

Do not create commits unless requested or required by the active workflow.

### 7. Report precisely

At completion, report:

- what changed and why;
- validation performed and its result;
- files and approximate diff size;
- any required scope expansion;
- follow-up suggestions clearly labeled **not included in this diff**.

## Decision Rules

- **Inside scope, verified, reversible:** proceed.
- **Unrelated improvement found:** leave it untouched and mention it only if useful.
- **Risky or forbidden area required:** explain why and ask for approval.
- **Diff unexpectedly large:** narrow it, or propose a split before continuing.
- **Multiple concerns are mechanically separable:** separate them.
- **Unrelated test failure appears:** determine whether this change caused it; do not silently fix pre-existing failures.
- **Correctness or security issue found nearby:** surface it immediately, but do not silently fold its fix into the current task.

## Guardrails

- Minimal means smallest **correct** change, not shortest patch.
- Every changed line must trace to the request, its tests, or cleanup necessitated by the change.
- Preserve existing behavior outside the requested scope.
- Never overwrite or revert changes you did not make.
- User-approved scope overrides are allowed, but record them explicitly.
