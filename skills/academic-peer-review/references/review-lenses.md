# Review lenses

Use the lenses relevant to the requested review depth and manuscript. These are checks within one review, not instructions to spawn separate reviewers.

## Contribution and framing

- Is the problem meaningful and the gap supported rather than asserted?
- Is the contribution specific, bounded, and distinguishable from implementation detail?
- Are novelty and generality claims proportional to the literature coverage and evidence?

## Methodology and design

- Does the design answer the stated question?
- Are assumptions, variables, units, inclusion criteria, controls, baselines, and procedures explicit?
- Are leakage, confounding, selection bias, measurement bias, and alternative explanations addressed?
- Could a qualified reader reproduce the analysis from the description and supplied artifacts?

## Statistics and quantitative evidence

When applicable, check:

- whether the test or model matches the design and data structure;
- independence, distributional assumptions, multiplicity, missing data, and stopping rules;
- effect sizes, uncertainty intervals, sample-size rationale, and sensitivity analysis;
- consistency among text, tables, figures, and supplementary results;
- whether “significant” is used statistically and whether practical significance is discussed.

Do not recompute results without the necessary data and code. Label plausibility checks separately from verified calculations.

## Results and interpretation

- Does every conclusion trace to reported evidence?
- Are causal statements justified by the design?
- Are null, negative, and contradictory results represented fairly?
- Are subgroup, ablation, robustness, or generalization claims adequately supported?
- Do figures show units, uncertainty, legends, sample definitions, and readable labels?

## Literature and citations

- Are relevant competing explanations and contrary findings represented?
- Does each citation support the attached claim rather than merely share a topic?
- Are preprints, published versions, corrections, and retractions distinguished?

Use `literature-review` when citations need external verification. Do not manufacture missing references during review.

## Ethics, transparency, and reproducibility

As applicable, check consent or approval statements, conflicts, funding, data/code availability, AI-use disclosure, image manipulation risk, privacy, dual use, and discipline-specific reporting requirements. Flag a missing statement; do not infer misconduct without evidence.

## Writing and presentation

Check organization, terminology, symbol consistency, internal cross-references, and whether the prose permits accurate interpretation. Keep copy-editing subordinate to scientific issues unless language blocks comprehension.
