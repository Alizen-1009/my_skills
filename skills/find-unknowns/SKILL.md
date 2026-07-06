---
name: find-unknowns
description: Run a structured discovery workflow to surface what the user does not yet know about a task before and during implementation — blindspots, ambiguous requirements, and unstated preferences — then hand off to the right follow-up skill such as interview, prototype, research, spec, planning, design, verification, or review. Use at the start of an unfamiliar or large task, when a plan keeps shifting, when the user cannot describe what they want, or before shipping a big change. Based on Thariq's "find your unknowns" methodology.
---

# Find Your Unknowns

## Overview

The gap between the user's description of a task (their prompt, context, references) and the real work (the codebase, its constraints, reality) is where **unknowns** live. When the agent hits an unknown, it guesses the user's intent. This skill's job is to shut down guessing: help the user discover and name their unknowns *before, during, and after* implementation, iteratively — not as a one-time upfront plan.

This is a toolbox, not a fixed pipeline. Diagnose first, then apply only the techniques that fit. Do not run all of them on a trivial task.

## The Four Unknowns

Classify what is missing before choosing a technique:

- **Known knowns** — already stated in the prompt.
- **Known unknowns** — the user knows they haven't decided this yet.
- **Unknown knowns** — too obvious to write down, but the user recognizes it on sight (often visual/UX taste).
- **Unknown unknowns** — never considered; the user doesn't know what they don't know.

## Step 0 — Diagnose

Before doing anything, decide which unknowns dominate, and pick techniques accordingly:

- Unfamiliar domain or unfamiliar corner of the codebase → **Blindspot scan** (unknown unknowns).
- Hard to describe, "I'll know it when I see it" → **Prototype** (unknown knowns).
- Direction is clear, details are fuzzy → **Interview the user** + **Draft a plan** (known unknowns).

Always give context about who the user is and what they already know — it sharpens every technique below.

## Hand Off to Other Skills

Use this skill as a discovery layer, not as the whole workflow. After naming the unknowns, pick the smallest follow-up skill that resolves the next uncertainty.

| Unknown or next need | Hand off to | Use when |
| --- | --- | --- |
| The user has not fully expressed intent | `interview-me` | Ask one question at a time until the underlying need is clear. |
| The plan needs pressure-testing | `grill-me` or `grill-with-docs` | Stress-test assumptions; use the docs variant when ADRs or glossary updates should be captured. |
| External facts are missing | `research` or `source-driven-development` | Gather primary-source evidence before deciding. |
| The user will know it when they see it | `prototype` | Show concrete options with fake data before committing to implementation. |
| The work needs a formal spec | `spec-driven-development` | Convert discovered constraints and decisions into a PRD/spec. |
| The work is too large to execute directly | `planning-and-task-breakdown` or `writing-plans` | Break the aligned spec into ordered, verifiable slices. |
| Interface boundaries are unclear | `api-and-interface-design` or `design-an-interface` | Decide API, module, or type contracts. |
| Codebase shape is the uncertainty | `codebase-design` or `improve-codebase-architecture` | Find the right module boundary, abstraction, or refactor direction. |
| UI behavior or visual quality is uncertain | `frontend-ui-engineering` | Turn chosen prototypes or preferences into production UI work. |
| A bug is present but the cause is unclear | `systematic-debugging` or `diagnosing-bugs` | Reproduce, isolate, hypothesize, instrument, and fix. |
| Implementation spans independent tasks | `subagent-driven-development` or `dispatching-parallel-agents` | Split work only when tasks do not share state or sequential dependencies. |
| Work appears complete | `verification-before-completion`, `requesting-code-review`, or `code-review` | Verify evidence, then review before claiming completion or merging. |

Before handing off, summarize:

- What is known now.
- What remains unknown.
- Which decision would change the implementation.
- Which artifact should carry forward: prototype, spec, plan, implementation notes, or acceptance report.

## Techniques by Phase

Each technique has a trigger and a ready-to-send prompt template. Adapt the bracketed parts.

### Explore (find the unknowns)

**1. Blindspot scan** — first move in an unfamiliar area.
> I'm adding [X] but I barely know the [Y] module in this codebase. Do a blindspot pass — find my "unknown unknowns" and explain them, so I can write you a better prompt.

**2. Prototype** — when it can't be described, show it. Use fake data, no backend.
> Before touching the real app, make an HTML file that mocks [the interface] with fake data. Give me 4 completely different design directions so I can see which feels right.

**3. Interview the user** — squeeze out the remaining fuzzy points.
> Ask me one question at a time. Target ambiguous areas, and prioritize questions whose answer would change the architecture.

### Plan (align intent)

**4. Show a reference** — the best reference is source code, not a screenshot.
> [path / library] implements the [behavior] I want. Read it, then re-implement the same semantics in [our stack].

**5. Draft a plan** — surface the decisions most likely to change, first.
> Write an HTML implementation plan, but put the decisions I'm most likely to adjust up top: data-model changes, new type interfaces, anything user-visible. Put mechanical refactors last — I trust you on those.

### Implement (catch unknowns that emerge mid-work)

**6. Notes as you go** — start a fresh session, feed in the spec/prototype, then:
> Maintain an implementation-notes.md. If an edge case forces you off the plan, choose the conservative option, record it under a "Deviations" section, and continue.

### Ship (align others, verify you understood)

**7. Handoff explainer**
> Package the prototype, spec, and implementation notes into one doc I can drop into chat for buy-in. Put a demo GIF at the top.

**8. Acceptance quiz** — the author's hard rule: pass it before merging.
> I want to be sure I understand this change fully. Make an HTML report with the change's context, intuition, and what was done — then a quiz at the bottom I have to pass.

## Operating Rules

- Whenever you're about to guess the user's intent, stop and apply the matching technique instead.
- Chain the artifacts: prototype → spec → implementation-notes → acceptance report; each is input to the next, so a new session doesn't lose context.
- For a small task, `blindspot scan + draft plan + acceptance quiz` already captures most of the value. Don't over-run.
