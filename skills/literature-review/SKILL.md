---
name: literature-review
description: Search and synthesize academic literature, identify research gaps, or verify scholarly citations and claim support. Match quick, narrative, scoping, or systematic review depth to the request.
---

# Literature Review

## Overview

Turn a research question into a transparent body of evidence. Keep search results, bibliographic identity, source content, and synthesis separate so that a real paper is never mistaken for proof of a claim it does not make.

Choose rigor proportionate to the request:

- **Quick scan**: orientation and candidate sources, not comprehensive.
- **Narrative review**: conceptually organized synthesis with an explicit search boundary.
- **Scoping review**: broad mapping of concepts, methods, and evidence gaps.
- **Systematic review**: predefined protocol, reproducible search and screening, and a documented study flow.

Use the label that matches the work actually performed.

## Integrity Rules

Apply three distinct checks to every important citation:

1. **Existence**: does the work and bibliographic record exist?
2. **Identity**: do title, authors, year, venue, DOI or other identifier refer to the same work?
3. **Claim support**: does the source text support the specific sentence, at the stated strength and scope?

Metadata APIs can establish existence and identity; they usually cannot establish claim support. Verify claim support from the abstract or full text, and record what was actually read. Never claim full-text verification after reading only metadata or an abstract.

Do not fabricate references or fill incomplete fields from memory. Mark unresolved fields as unverified. Treat search-result snippets and AI summaries as discovery aids, not primary evidence.

## Workflow

For a citation check or quick scan, answer the bounded question directly with sources and read scope. Use the search logs, screening protocol, and evidence matrix below for multi-study reviews when they serve the requested rigor. Stop once the requested coverage and claim verification are met; broaden only for unresolved gaps. Reuse already verified records rather than repeating lookups.

### 1. Frame the question

Capture enough structure to search accurately:

- population, system, phenomenon, or domain;
- intervention, method, exposure, or focal concept;
- comparator when relevant;
- outcomes or evidence sought;
- time range, language, study type, and disciplinary boundary;
- intended review type and stopping condition.

Translate the question into several concept groups and list synonyms, abbreviations, spelling variants, and controlled vocabulary where available.

### 2. Select sources

Match databases to the field. Prefer primary, stable sources:

- publisher pages and DOI registries for bibliographic identity;
- PubMed or PMC for biomedical literature;
- Crossref and OpenAlex for broad metadata and citation discovery;
- Semantic Scholar for discovery, not final authority;
- arXiv and discipline repositories for clearly labeled preprints;
- field-specific indexes or the user's institutional databases when required.

Before sending unpublished titles, abstracts, queries, or private material to an external service, tell the user what will be transmitted when that is not already obvious from the request.

### 3. Search transparently

For a reproducible review, record for each database:

- database or endpoint;
- exact query;
- filters and date searched;
- number of results inspected or retrieved;
- limitations, access failures, and deduplication method.

Use multiple query formulations when terminology varies. For reviews that claim completeness, add backward citation chasing, forward citation chasing, and a documented update search.

### 4. Screen against explicit criteria

Define inclusion and exclusion criteria before screening large result sets. Screen titles and abstracts first, then full text where available. Record exclusion reasons at the appropriate stage.

Deduplicate using stable identifiers first, then normalized title, year, and author checks. Do not merge records solely because titles look similar.

For a systematic review, preserve counts needed for a PRISMA-style flow. Do not invent counts for inaccessible or unperformed stages.

### 5. Build an evidence matrix

Use a table with fields appropriate to the question. A useful default is:

| Field | Purpose |
| --- | --- |
| Citation key and stable identifier | Trace the work |
| Publication type and version | Distinguish preprint, conference, journal, correction |
| Research question and context | Establish relevance |
| Design, sample or dataset | Judge applicability |
| Method and comparator | Compare approaches |
| Outcomes and uncertainty | Capture actual evidence |
| Main findings | Summarize without strengthening |
| Limitations and bias risks | Bound interpretation |
| Read scope | Metadata, abstract, sections, or full text |
| Claim locator | Page, section, table, figure, or quoted passage |
| Verification status | Verified, partially verified, or unresolved |

Preserve negative, null, and contradictory findings. Missing details remain missing; they are not an invitation to infer.

### 6. Synthesize, do not catalogue

Organize the review around concepts, methods, evidence patterns, or disagreements. For each theme:

1. state the bounded synthesis claim;
2. identify converging and conflicting evidence;
3. explain differences in design, population, measurement, assumptions, or version;
4. assess confidence and transferability;
5. identify the remaining gap without claiming novelty from absence alone.

A gap is stronger when it follows from explicit coverage analysis, contradictory evidence, or a methodological limitation—not merely because the current search did not find a paper.

### 7. Verify the final citations

Before delivery:

- resolve unverified DOI values through `https://doi.org/` or authoritative metadata;
- reconcile discrepancies in title, author, year, and venue across records;
- distinguish preprints from published versions and use the intended version;
- inspect retractions, corrections, or expressions of concern when material;
- map every substantive literature claim to supporting source text;
- lower the claim strength or mark it unresolved if support cannot be checked.

External search success is not proof of correctness. Report inaccessible databases, paywalls, API limits, date cutoffs, and unverified sources.

## Outputs

Match the output to the request. Common deliverables are:

- search strategy and search log;
- screened bibliography;
- evidence matrix;
- thematic synthesis;
- research-gap analysis;
- citation verification report;
- PRISMA-style counts when a systematic process was actually followed;
- manuscript-ready related-work draft, coordinated with `academic-writing`.

End with a concise limitations section stating search coverage, read scope, date boundary, and unresolved verification issues.
