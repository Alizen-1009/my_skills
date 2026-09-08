---
name: find-unknowns
description: Surface consequential unknowns when requirements keep changing, preferences are hard to express, or the user requests a discovery or blindspot pass.
---

# Find Your Unknowns

Use the smallest technique that resolves a decision likely to change the outcome. Routine implementation details can be inferred from context; unfamiliarity alone does not require an interview or a new artifact.

## Choose a technique

- **Blindspot scan:** inspect the relevant code or domain constraints and identify assumptions that could invalidate the approach.
- **Prototype:** when the user needs to see options to choose, use a disposable mock with fake data. Agree on the direction before integrating it.
- **Focused question:** ask about the highest-impact missing decision, while continuing independent authorized work.
- **Targeted research:** check external facts that affect the decision; stop when the uncertainty is resolved or report the evidence gap.
- **Plan:** for interdependent work, put architecture-changing decisions before mechanical steps.

Report the consequential unknown, what is already known, and the next action that resolves it. Do not manufacture uncertainty to fill a taxonomy.

## Optional follow-ups

Use `prototype` for a throwaway design experiment, `codebase-design` for module boundaries, or `diagnosing-bugs` for a hard unexplained failure when that specialized workflow is needed. Otherwise continue the task directly rather than chaining skills.

Create a spec, implementation-notes file, handoff report, or acceptance quiz only when requested or needed by the project's workflow. A discovery pass is complete when the blocking decisions are resolved or clearly identified; it is not an automatic approval gate before implementation or merging.

Adapted from Thariq's “find your unknowns” methodology.
