---
name: minimal-diff
description: Audit patch scope and reversibility when the user requests a minimal diff or a change is expanding beyond its intended scope.
license: Apache-2.0
---

# Minimal Diff

Optimize for the smallest correct, reviewable change, not the fewest lines.

## Audit

- Establish the requested outcome and any actual protected boundaries from the task and repository. Do not invent forbidden file categories.
- Inspect the relevant diff and worktree status. Every changed hunk should serve the request, its verification, or cleanup made necessary by the change.
- Remove your own unrelated cleanup; preserve pre-existing user changes. Include prerequisites needed for correctness rather than under-fixing to meet a size target.
- If scope grows unexpectedly, seek a narrower solution or separable changes. File and line counts are context, not approval thresholds.
- Check whether reverting this change would restore prior behavior. For data migrations or other persistent side effects, identify recovery requirements without running destructive reverts as a test.

Proceed with authorized, reversible work. Ask before destructive or external actions outside existing authorization. Configuration, dependencies, and public interfaces are not automatically forbidden when their changes are necessary to the request.

## Completion

Review the final diff, run `git diff --check` and the checks relevant to the changed behavior, plus repository-required validation. Passing checks need not be repeated without a new reason. Report material scope expansion, validation results, and unresolved risks concisely.

Keep distinct concerns separable when practical. Create commits only when requested or required by the active workflow.
