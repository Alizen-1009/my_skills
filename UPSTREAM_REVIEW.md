# Upstream update review

This records the reviewed update batch associated with the current submodule diff. Revisions are fixed commits, not floating branches. No upstream hooks, installers, benchmarks, Office tools, MCP migrations, or deployment commands were executed during this update.

## Decisions

| Source | Previous checkout | Reviewed remote head | Decision |
| --- | --- | --- | --- |
| addyosmani-agent-skills | `6ca0cd7db39b` | `8c99fa36d900` | Upgrade. Selected skills receive corrected examples, safer secret scanning, and skill-local performance/security references. Explicitly exclude new `accessibility-engineering` to avoid silently expanding selection. |
| anthropics-skills | `41bbe19d1a1a` | `e4bb5d960d87` | Upgrade. Office/PDF fixes, Apache-2.0 Office/PDF licensing, and MCP SDK guidance improvements. Compatibility caveats below. |
| goutoujunshi | `4ced1d575615` | `6db7354a4002` | Upgrade. Only README installation wording changed; skill behavior is unchanged. The README now names a different download URL; this repository retains its existing configured source. |
| mattpocock-skills | `3cca18b368ae` | `abeeaf9` | Hold. Upstream deletes selected `resolving-merge-conflicts`, renames CONTEXT conventions to GLOSSARY, and adds unreviewed skills that exclusion-based discovery would select. Handle that migration separately rather than changing the existing set incidentally. |
| supervisor-skills | `207bc6f7a1aa` | `364d96236dab` | Hold. `drawio-reconstruction` moves from `skills/` to `others/`; `figure-designer` frontmatter changes from CC-BY-4.0 to CC-BY-NC-SA-4.0. Resolve selection paths and licensing before upgrading. |
| ai-infra-auto-driven-skills | `8173704776db` | `548ef046a5e0` | Hold. Updates affect the excluded video skill and its tests, not the ten selected skills. Existing layout and licensing caveats in README still apply. |
| karpathy-guidelines | `2c606141936f` | `2c606141936f` | Unchanged; already current and excluded. |
| humanizer | `b48c832f0f80` | `a32f24407364` | Preserve the pre-existing local checkout change. Parent repository already recorded `a32f24407364`, while the user's working checkout was `b48c832f0f80`; do not silently reset or accept that unrelated pin change. |

The main repository's submodule entries record the complete revisions for the three upgrades. Commit the reviewed pins together with the selection and catalog changes so normal bootstrap restores the reviewed versions. The unrelated local `humanizer` checkout change is not part of this update.

## Compatibility and authorization notes

- Addy's examples include npm package downloads, browser audits, and a credentialed Vercel rollback with `--yes`. They are examples, not permission to install toolchains, deploy, or contact production. Repository/user authorization boundaries still govern execution. No such command ran here.
- Anthropic's `xlsx` recalculation now preserves workbook parts by transferring cached values from a recalculated copy. `status: success` does **not** mean every formula was computed: inspect `not_computed`, stale caches, and fallback values. Some unsupported XML structures are refused. Runtime checks with real Office applications were not performed in this batch.
- `mcp-builder` now distinguishes SDK v1/v2, defaults new projects to v2, and keeps existing v1 projects on v1 unless migration is requested. Verify package/API availability before using templates. The `@latest` migration codemod is not run automatically.
- PPTX text extraction now uses `python-pptx`; theme helpers may require `jszip` resolution. No optional dependencies were provisioned here.
- Office rendering/recalculation is not a network sandbox. Treat untrusted documents and external relationships accordingly.

## Added local capability

`skills/blast-radius/` is a compact, manually invoked adaptation, not a new pstack submodule or plugin installation. Attribution and the reviewed upstream revision are in [THIRD_PARTY.md](THIRD_PARTY.md). No `poteto-mode` or benchmark skill was added.

## Selection and local installation

The resulting set is 57 skills, including eight marked manual-only. See [SKILL_TRIGGERS.md](SKILL_TRIGGERS.md). Existing selection is preserved apart from the deliberate addition of `blast-radius`.

Before replacing the local Pi copies, the previous skills directory was backed up outside this repository under the Pi agent home's `backups/skills-before-upstream-update-*` directory. The installer then reconciled all selected skills, including ten AI infrastructure skills already selected in the manifest but previously missing locally. No Codex or Claude installation was changed. Reload or restart Pi to discover the new set.

## Verification

- Personal-skill validation.
- Catalog regeneration and consistency check.
- Installer dry-run, including explicit replacement preview.
- Repository unittest suite, including the updated selection count and manual-only set regression test.
- Post-install comparison of all selected source trees against their installed copies.

These checks verify repository selection and installation, not the end-to-end behavior of every upstream workflow, external SDK, GPU environment, or Office runtime.
