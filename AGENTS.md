# AGENTS.md

## Repository purpose

This repository is the portable, secret-free source of truth for the owner's Pi coding-agent setup across machines. It pins the Pi CLI and Pi packages, merges portable configuration from `pi-config/`, and installs personal plus curated upstream skills.

Preserve these boundaries when changing it:

- Keep reproducible Pi settings in `pi-config/settings.patch.json`; it merges into local `settings.json` and must not manage the dynamic `packages` list or machine-specific skill paths.
- Keep extension configuration under `pi-config/` using paths relative to `~/.pi/agent/`.
- Pin Pi and package versions in `pi-packages.json`; bootstrap must remain safe and idempotent.
- Keep personal skills under `skills/`; filter upstream submodule skills through `skill-sources.json` rather than editing upstream copies. Regenerate `SKILLS.md` with `python3 scripts/install-skills.py --write-catalog` whenever the selection changes.
- Never commit `auth.json`, sessions, trust decisions, caches, literal API keys, cookies, or machine-specific private paths. Credentials remain a manual new-machine `/login` step.
- Verify installer behavior with the Python test suite and validate personal skills before finishing.

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Find Your Unknowns Before Committing

**Don't guess intent. Surface what you don't know while it's still cheap to change.**

The gap between the ask and the real work is where unknowns live. Close it before and during implementation, not after:

- Unfamiliar area or domain? Do a blindspot pass for "unknown unknowns" before writing the real prompt.
- Can't describe it? Prototype with fake data and let me pick from options - don't spec it in prose.
- Direction clear, details fuzzy? Interview me one architecture-changing question at a time.
- About to start? Draft a plan that puts the decisions most likely to change up top.
- Big change done? Produce an acceptance quiz and don't merge until I pass it.

Reach for the `find-unknowns` skill (`$find-unknowns`) to run this as a toolbox - use only the moves that fit, skip it on trivial tasks.

The test: whenever you're about to assume what I want, stop and pick the matching move instead.

## 3. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 4. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 5. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.