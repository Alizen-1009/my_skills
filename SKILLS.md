# 已安装 Skills 清单

> 此文件由 `python3 scripts/install-skills.py --write-catalog` 自动生成，请勿手工维护。

当前默认安装集共 **44** 个 Skills。

## 来源统计

| 来源 | 数量 |
| --- | ---: |
| local | 6 |
| https://github.com/mattpocock/skills | 15 |
| https://github.com/addyosmani/agent-skills | 9 |
| https://github.com/anthropics/skills | 11 |
| https://github.com/powerycy/goutoujunshi.git | 1 |
| https://github.com/HKUSTDial/Supervisor-Skills.git | 2 |

## Skills

### local

| Skill | 调用方式（Pi） | Description |
| --- | --- | --- |
| `academic-peer-review` | 自动或手动 | Diagnose academic manuscript quality, methodology, statistics, or revision completeness when the user requests peer review or publication-readiness assessment. Read-only unless revision is requested. |
| `academic-writing` | 自动或手动 | Draft, revise, translate, or polish academic manuscript prose and reviewer responses without inventing evidence. For source searching or diagnostic peer review, use the corresponding skill. |
| `find-unknowns` | 自动或手动 | Surface consequential unknowns when requirements keep changing, preferences are hard to express, or the user requests a discovery or blindspot pass. |
| `literature-review` | 自动或手动 | Search and synthesize academic literature, identify research gaps, or verify scholarly citations and claim support. Match quick, narrative, scoping, or systematic review depth to the request. |
| `minimal-diff` | 自动或手动 | Audit patch scope and reversibility when the user requests a minimal diff or a change is expanding beyond its intended scope. |
| `personal-skill-authoring` | 自动或手动 | Create, adapt, or maintain personal skills in this repository, including structure, triggers, and local validation. |

### https://github.com/mattpocock/skills

| Skill | 调用方式（Pi） | Description |
| --- | --- | --- |
| `codebase-design` | 自动或手动 | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary. |
| `diagnosing-bugs` | 自动或手动 | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. |
| `domain-modeling` | 自动或手动 | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR. |
| `grill-with-docs` | **仅手动调用**：`/skill:grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `grilling` | 自动或手动 | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. |
| `handoff` | **仅手动调用**：`/skill:handoff` | Compact the current conversation into a handoff document for another agent to pick up. |
| `prototype` | 自动或手动 | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like. |
| `resolving-merge-conflicts` | 自动或手动 | Use when you need to resolve an in-progress git merge/rebase conflict. |
| `setup-pre-commit` | 自动或手动 | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing. |
| `wayfinder` | **仅手动调用**：`/skill:wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. |
| `wizard` | 自动或手动 | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself. |
| `writing-beats` | **仅手动调用**：`/skill:writing-beats` | Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it. |
| `writing-for-agents` | 自动或手动 | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |
| `writing-fragments` | **仅手动调用**：`/skill:writing-fragments` | Writing, explore: mine raw fragments, no structure yet. |
| `writing-shape` | **仅手动调用**：`/skill:writing-shape` | Writing, exploit: shape raw material into an article, paragraph by paragraph. |

### https://github.com/addyosmani/agent-skills

| Skill | 调用方式（Pi） | Description |
| --- | --- | --- |
| `api-and-interface-design` | 自动或手动 | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend. |
| `ci-cd-and-automation` | 自动或手动 | Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates, configure test runners in CI, or establish deployment strategies. |
| `deprecation-and-migration` | 自动或手动 | Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use when migrating a database schema in production, such as renaming or dropping a column without downtime (expand/contract). Use when deciding whether to maintain or sunset existing code. |
| `frontend-ui-engineering` | 自动或手动 | Builds production-quality, accessible, responsive user-facing UIs. Use when building or modifying interfaces and pages, creating components, implementing layouts, meeting WCAG accessibility requirements, managing state, or when the output needs to look and feel production-quality rather than AI-generated. |
| `idea-refine` | 自动或手动 | Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one. Triggers on "ideate", "refine this idea", or "stress-test my plan". |
| `observability-and-instrumentation` | 自动或手动 | Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use when shipping any feature that runs in production and you need evidence it works. Use when production issues are reported but you can't tell what happened from the available data. |
| `performance-optimization` | 自动或手动 | Optimizes application performance across frontend, backend, queries, and databases. Use when performance requirements exist, when you suspect performance regressions, when Core Web Vitals or load times need improvement, when N+1 query patterns need fixing, or when profiling reveals bottlenecks. |
| `security-and-hardening` | 自动或手动 | Hardens code against vulnerabilities. Use when auditing an input handler for vulnerabilities, when handling user input, authentication, data storage, or external integrations, or when checking a login flow is safe against the OWASP Top Ten. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services. Use when auditing dependencies for known vulnerabilities, triaging package-manager audit findings, or assessing supply-chain risk in a new package. Use when personal data or privacy compliance (GDPR, CCPA) is involved. |
| `shipping-and-launch` | 自动或手动 | Prepares production launches. Use when preparing to deploy to production, or when asking what needs to be in place before shipping. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy. |

### https://github.com/anthropics/skills

| Skill | 调用方式（Pi） | Description |
| --- | --- | --- |
| `canvas-design` | 自动或手动 | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations. |
| `doc-coauthoring` | 自动或手动 | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks. |
| `docx` | 自动或手动 | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation. |
| `frontend-design` | 自动或手动 | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults. |
| `mcp-builder` | 自动或手动 | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK). |
| `pdf` | 自动或手动 | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill. |
| `pptx` | 自动或手动 | Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx or .potx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates (.potx), layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx or .potx filename, regardless of what they plan to do with the content afterward. If a .pptx or .potx file needs to be opened, created, or touched, use this skill. |
| `slack-gif-creator` | 自动或手动 | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack." |
| `theme-factory` | 自动或手动 | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly. |
| `webapp-testing` | 自动或手动 | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. |
| `xlsx` | 自动或手动 | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved. |

### https://github.com/powerycy/goutoujunshi.git

| Skill | 调用方式（Pi） | Description |
| --- | --- | --- |
| `goutoujunshi` | 自动或手动 | 恋爱军师与情绪支持 skill。用于心动、暧昧、追求、聊天记录或截图分析、约会、关系确认、多人选择、冲突、冷淡、投入失衡、分手、复合、出轨、婚姻或家庭问题；也用于分析关系信号、设计主动推进或退出策略、润色可直接发送的话术，以及把冷读、自然流、Blueprint、Mystery 等经典社交体系转译成真实、互惠、可退出的沟通能力。支持分析ChatLab已有数据和经同意可撤销的长期关系档案，不负责导出聊天软件数据。首次使用时为用户及一个或多个目标对象建立包含 MBTI、主观综合评分和关系背景的档案。 |

### https://github.com/HKUSTDial/Supervisor-Skills.git

| Skill | 调用方式（Pi） | Description |
| --- | --- | --- |
| `drawio-reconstruction` | 自动或手动 | Reconstructs reference images into high-fidelity, editable Draw.io files with rendered previews: native Draw.io elements carry text and structure, SVG covers simple icons that match the reference, and cropped or transparent PNGs preserve complex visuals. Use when the user wants a diagram image, research figure, architecture diagram, slide, UI screenshot, or image folder turned into `.drawio` XML; batch requests use a manifest with bounded parallelism when available and a full-fidelity serial fallback otherwise. |
| `figure-designer` | 自动或手动 | Advises on the design of the three core figures in a technical paper: the Motivated Example (Figure 1), the Solution Overview (Methodology), and the Experimental Results figures. Recommends the right design paradigm, layout, labelling, and tool for each figure type, then runs a quality-control audit. Use when the user asks to 'design a figure', 'draw Figure 1', 'plot experiment results', 'choose the right chart type', 'which figure tool to use', or 'figure looks unprofessional'. |
