---
name: academic-peer-review
description: Diagnose academic manuscript quality, methodology, statistics, or revision completeness when the user requests peer review or publication-readiness assessment. Read-only unless revision is requested.
---

# Academic Peer Review

## Overview

Review a manuscript as a diagnostic instrument, not as a performance. Identify consequential problems, connect each finding to manuscript evidence, and propose the smallest useful remedy. Do not claim to represent a real journal, editor, ethics board, or domain expert whose qualifications are not available.

Keep review and revision separate. The default output is findings and recommendations; use `academic-writing` only when the user asks to implement changes.

## Establish the Review Contract

Determine:

- manuscript type, discipline, stage, and target venue if known;
- requested depth: quick assessment, full review, methodology focus, statistical focus, or revision verification;
- materials available: manuscript, supplement, data, code, reporting checklist, reviewer comments, and response letter;
- whether access is complete or limited to excerpts.

State material limitations before drawing conclusions. Do not infer that an absent supplement, dataset, or section does not exist when it may simply not have been provided.

## Evidence Standard for Findings

Every major finding should contain:

1. **Location**: section, page, paragraph, table, figure, equation, or quoted phrase.
2. **Observation**: what the manuscript actually says or omits.
3. **Consequence**: why this affects validity, reproducibility, interpretation, or presentation.
4. **Requested action**: a concrete and proportionate fix or clarification.

Separate verified defects from questions and suggestions. Do not turn a stylistic preference into a validity claim.

Use severity consistently:

- **Critical**: threatens research integrity, participant safety, legal or ethical compliance, or makes the central evidence unusable.
- **Major**: could change the main conclusion, method validity, reproducibility, or interpretation.
- **Minor**: localized clarity, reporting, consistency, or presentation issue that does not alter the central conclusion.
- **Suggestion**: optional improvement, not a condition for validity.

## Review Workflow

### 1. Reconstruct the paper's own case

Before criticizing, summarize neutrally:

- research question and claimed gap;
- design, method, data, and comparator;
- principal results;
- claimed contribution;
- stated limitations.

Check that the abstract, main text, figures, tables, and conclusion tell the same story.

### 2. Review at the requested depth

For a full review or a focused methodology/statistics audit, read [review lenses](references/review-lenses.md) and apply the relevant sections. For a quick assessment or a bounded revision check, inspect the requested issue directly; do not expand into every lens or external literature search without a concrete need.

Do not pretend that one model represents multiple independent human reviewers. Never claim to have checked unavailable data, calculations, or sources.

### 3. Challenge the strongest interpretation

Stress-test the central claim:

- What plausible alternative explanation remains?
- What evidence would falsify the claim?
- Which conclusion depends most heavily on an unverified assumption?
- Does the paper generalize beyond its sample, dataset, apparatus, or operating conditions?

Then perform a fairness pass: remove criticisms already answered by the manuscript and acknowledge genuine strengths or safeguards.

### 4. Verify a revision when requested

For a re-review, build a traceability table:

| Reviewer concern | Author response | Manuscript change | Evidence checked | Status |
| --- | --- | --- | --- | --- |

Use statuses such as `resolved`, `partially resolved`, `not resolved`, or `cannot verify`. Check the manuscript change itself rather than accepting the response letter's description. Also look for regressions or claim drift introduced by the revision.

## Output Format

For a quick or focused review, lead with findings and material limitations; omit empty sections. For a full report, use this default structure unless the user or venue asks for another:

```markdown
# Review summary
[Neutral summary of question, method, evidence, and contribution]

# Overall assessment
[Most important strengths, limitations, and confidence bounded by available materials]

# Major findings
## M1. [Finding title]
- Severity: Major
- Location: ...
- Observation: ...
- Consequence: ...
- Requested action: ...

# Minor findings
## m1. [Finding title]
...

# Questions for the authors
...

# Recommendation
[Conditional recommendation and rationale, if requested]

# Review limitations
[Materials not reviewed, expertise limits, and checks not performed]
```

Do not produce a numeric score or accept/reject recommendation unless the user or review form requires it. When one is required, explain that it is advisory and tie it to explicit criteria rather than false precision.

## Final Quality Check

Before delivery, verify that:

- each major criticism is grounded in a location and consequence;
- severities reflect impact rather than tone;
- findings do not contradict one another;
- the review distinguishes missing reporting from flawed execution;
- no unavailable data, source, or calculation is described as inspected;
- recommendations are feasible and proportionate;
- confidential or unpublished material is not sent to external services without the user's awareness.
