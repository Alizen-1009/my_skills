---
name: academic-writing
description: Draft, revise, translate, or polish academic manuscript prose and reviewer responses without inventing evidence. For source searching or diagnostic peer review, use the corresponding skill.
---

# Academic Writing

## Overview

Help the user produce precise academic prose without inventing evidence. Match the amount of process to the task: revise a paragraph directly when the request is narrow; clarify the argument and evidence before drafting when the request changes claims, spans several sections, or starts a manuscript from scratch.

Default to Chinese academic expression when the user writes in Chinese, while preserving English paper titles, established terms, formulas, variables, software commands, citations, and reference entries.

## Evidence Boundary

Classify substantive material before relying on it:

- **Provided evidence**: text, data, results, figures, tables, references, or reviewer comments supplied by the user.
- **User-confirmed context**: facts or decisions the user explicitly confirms.
- **Inference**: a conclusion reasonably drawn from the supplied material but not directly reported.
- **Suggestion**: a possible extension, experiment, explanation, or framing that is not yet evidence.

Keep these categories distinct. Inferences and suggestions may guide revision, but must not silently become manuscript facts.

Never invent citations, authors, DOI values, venues, sample sizes, parameters, statistical significance, experimental results, page numbers, or claims attributed to a source. Mark unsupported placeholders clearly, for example `[需要实验结果]` or `[需要文献支持]`.

## Workflow

### 1. Scope the request

Determine only the details that materially change the output:

- target section and purpose;
- target venue, thesis requirement, audience, language, and length when relevant;
- whether the task is drafting, substantive revision, copy-editing, translation, compression, or reviewer response;
- available evidence and non-negotiable terminology.

Do not force a planning interview for a local edit. If missing information would change a central claim, ask one focused question or proceed with an explicit placeholder.

### 2. Build the argument before long-form drafting

For a new section or substantial rewrite, establish:

1. the question or problem;
2. the gap or tension;
3. the proposed method or position;
4. the evidence available;
5. the contribution that the evidence actually supports;
6. limitations and applicability conditions.

For small edits, infer this structure from the surrounding text and preserve the author's intended meaning.

### 3. Draft by rhetorical function

Use the user's template when supplied. Otherwise use these defaults as guidance, not rigid formulas:

- **Abstract**: problem, method, evidence or data, key result, bounded contribution.
- **Introduction**: context, unresolved gap, significance, approach, supported contributions.
- **Related work**: organize by technical or conceptual theme; compare assumptions, evidence, and limitations rather than listing papers.
- **Methods**: assumptions, variables, units, procedure, implementation details, and reproducibility conditions.
- **Results**: report observations and uncertainty before interpretation; tie every quantitative claim to a table, figure, or supplied result.
- **Discussion**: interpret mechanisms and implications, compare with prior work, then state limitations and alternatives.
- **Conclusion**: answer the research question at the strength allowed by the evidence; do not introduce new results.
- **Reviewer response**: quote or identify the concern, state the action, locate the change, provide evidence, and disagree respectfully when necessary.

### 4. Revise for precision

Check each paragraph for one clear function and a logical connection to the section's purpose. Replace unsupported labels such as “显著”“先进”“有效”“鲁棒” with measured conditions, comparison baselines, uncertainty, or more modest wording.

Preserve:

- causal versus correlational strength;
- uncertainty and hedging justified by the evidence;
- formulas, units, assumptions, and applicability conditions;
- terminology and symbols used consistently across sections;
- the user's voice unless a different register is requested.

Do not treat generic bans on transition words as style rules. Remove a phrase only when it is repetitive, empty, or obscures the argument.

### 5. Verify before delivery

Compare the revision against the source material:

- no number, citation, method detail, or conclusion was added without support;
- no qualifier or limitation was accidentally removed;
- citations remain attached to the claims they support;
- the requested length, language, and format are satisfied;
- unresolved evidence gaps are visible.

## Coordination

Use `literature-review` when the task requires finding, screening, or synthesizing sources. Use `academic-peer-review` when the user wants an evaluative review rather than manuscript drafting. If the final deliverable is `.docx`, `.pptx`, `.pdf`, or a spreadsheet, also use the corresponding file-format skill; this skill governs the manuscript prose, not the file mechanics.

## Delivery

Provide the requested text first. Then briefly state, when applicable:

- what was substantively changed;
- which supplied evidence was used;
- which claims still require data or citation support;
- any ambiguity that could change the scientific meaning.
