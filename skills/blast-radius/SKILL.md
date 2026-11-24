---
name: blast-radius
description: Audit a change's hidden downstream risks and test the assumptions its safety depends on.
disable-model-invocation: true
license: MIT
---

# Blast radius

Audit the supplied diff, commit, or proposed change for effects outside the edited lines. This is an opt-in review, not a default gate for every edit.

## Trace the impact

- Read the change and describe the behavioral difference, including effects not obvious from the diff.
- Identify the key assumptions its safety depends on. There may be more than one; do not force unrelated risks into a single explanation.
- Follow callers and less visible contracts: serialized data, API consumers, database schemas, feature flags, lifecycle ordering, concurrent actors, and downstream readers in other languages.
- Inspect the actual pinned dependency version and local patches when library behavior matters. Cite real source locations rather than inventing callers or inferring safety from an empty symbol search.

## Test the safety assumptions

For each consequential assumption, separate source evidence, reasoning, and runtime evidence. Prefer the cheapest safe check that exercises the real behavior: an existing regression test, a disposable script importing the actual code, or an authorized application repro.

Run relevant checks when the environment permits. Record the command, result, and what it does not establish. Mark an assumption **unproven** when it cannot be checked; passing compilation alone does not establish runtime safety. Avoid speculative numeric probabilities.

Keep review read-only by default. Disposable probes must avoid overwriting user work. Ask before destructive checks, production access, or external writes not already authorized. Propose fixes and persistent regression tests without implementing them unless requested. Use independent reviewers only when the impact or uncertainty warrants the cost; no particular agent or model is required.

## Report

- What changed and which consumers or contracts are affected.
- The safety assumptions, each supported by source or runtime evidence, or marked unproven.
- Confirmed risks, with source locations, consequences, and a repro or next check.
- Suspected risks still unresolved, distinguished from findings.
- Risks checked and cleared, plus any essential check remaining before merge.

Keep the report proportional to the change and remove secrets from shared evidence. Do not merge, publish, or open a PR as part of this review.
