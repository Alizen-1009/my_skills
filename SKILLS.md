# 已安装 Skills 清单

本清单基于 `python3 scripts/install-skills.py --list` 生成，并将用途说明整理为中文摘要。

当前可安装 skills 总数：**64**。

## 来源统计

| 来源 | 数量 |
| --- | ---: |
| https://github.com/addyosmani/agent-skills | 24 |
| https://github.com/mattpocock/skills | 38 |
| local | 2 |

## Skills 列表

| Skill | 来源 | 作用 |
| --- | --- | --- |
| `api-and-interface-design` | https://github.com/addyosmani/agent-skills | 设计稳定 API、模块边界和类型契约，适合 REST、GraphQL、前后端接口和公共接口设计。 |
| `ask-matt` | https://github.com/mattpocock/skills | 帮你判断当前任务应该使用哪个 Matt Pocock skill 或 workflow。 |
| `browser-testing-with-devtools` | https://github.com/addyosmani/agent-skills | 用 Chrome DevTools MCP 做真实浏览器测试、DOM 检查、控制台错误和网络请求分析。 |
| `ci-cd-and-automation` | https://github.com/addyosmani/agent-skills | 设置或修改 CI/CD、质量门禁、自动化测试和部署流程。 |
| `claude-handoff` | https://github.com/mattpocock/skills | 把当前上下文交接给新的后台 agent 继续处理。 |
| `code-review` | https://github.com/mattpocock/skills | 从指定基线开始做双轴代码审查：代码标准和需求符合度。 |
| `code-review-and-quality` | https://github.com/addyosmani/agent-skills | 合并前做多维代码质量审查，关注 bug、风险、可维护性和测试缺口。 |
| `code-simplification` | https://github.com/addyosmani/agent-skills | 在不改变行为的前提下简化复杂代码，提升清晰度和可维护性。 |
| `codebase-design` | https://github.com/mattpocock/skills | 用深模块、清晰边界和可测试接口的方式改进代码库设计。 |
| `context-engineering` | https://github.com/addyosmani/agent-skills | 优化 agent 的项目上下文、规则文件和工作入口，减少上下文质量问题。 |
| `debugging-and-error-recovery` | https://github.com/addyosmani/agent-skills | 系统化排查测试失败、构建失败、异常行为和错误恢复。 |
| `deprecation-and-migration` | https://github.com/addyosmani/agent-skills | 管理旧系统、旧 API、旧功能的弃用、迁移和下线策略。 |
| `design-an-interface` | https://github.com/mattpocock/skills | 用多个并行 agent 生成不同接口设计方案，适合探索模块 API。 |
| `diagnosing-bugs` | https://github.com/mattpocock/skills | 针对困难 bug、性能回退和失败行为做诊断循环。 |
| `documentation-and-adrs` | https://github.com/addyosmani/agent-skills | 记录架构决策、ADR、公共 API 变化和未来维护者需要的上下文。 |
| `domain-modeling` | https://github.com/mattpocock/skills | 建立和打磨领域模型、术语表和统一语言。 |
| `doubt-driven-development` | https://github.com/addyosmani/agent-skills | 对重要决策做 fresh-context 对抗式复核，适合高风险或不熟悉代码场景。 |
| `edit-article` | https://github.com/mattpocock/skills | 编辑文章，优化结构、表达清晰度和行文紧凑度。 |
| `find-unknowns` | local | 在大任务或模糊任务开始前找出未知点、盲区、含糊需求和未声明偏好，并把结果交给访谈、原型、规格、计划、设计、验证或 review 类 skills。 |
| `frontend-ui-engineering` | https://github.com/addyosmani/agent-skills | 构建生产级前端 UI，关注布局、交互、状态管理和视觉质量。 |
| `git-guardrails-claude-code` | https://github.com/mattpocock/skills | 给 Claude Code 设置 git 安全 hooks，阻止危险命令如 push、reset --hard、clean。 |
| `git-workflow-and-versioning` | https://github.com/addyosmani/agent-skills | 管理 git 工作流、分支、提交、版本号、标签和 changelog。 |
| `grill-me` | https://github.com/mattpocock/skills | 通过高强度追问打磨计划或设计。 |
| `grill-with-docs` | https://github.com/mattpocock/skills | 一边追问打磨计划，一边沉淀 ADR 和术语文档。 |
| `grilling` | https://github.com/mattpocock/skills | 当用户想压力测试一个计划或设计时，进行系统追问。 |
| `handoff` | https://github.com/mattpocock/skills | 把当前对话压缩成交接文档，方便其他 agent 接手。 |
| `idea-refine` | https://github.com/addyosmani/agent-skills | 把模糊想法通过发散和收敛变成清晰可执行方案。 |
| `implement` | https://github.com/mattpocock/skills | 根据 PRD 或 issue 集合执行实现工作。 |
| `improve-codebase-architecture` | https://github.com/mattpocock/skills | 扫描代码库架构改进机会，生成可视化报告并逐项追问。 |
| `incremental-implementation` | https://github.com/addyosmani/agent-skills | 用小步提交和可验证切片交付功能，避免一次性大改。 |
| `interview-me` | https://github.com/addyosmani/agent-skills | 对不清楚的需求做一问一答访谈，直到用户真实意图足够明确。 |
| `loop-me` | https://github.com/mattpocock/skills | 在当前 workspace 内反复追问你想构建的 workflow 规格。 |
| `migrate-to-shoehorn` | https://github.com/mattpocock/skills | 把测试里的 `as` 类型断言迁移到 `@total-typescript/shoehorn`。 |
| `observability-and-instrumentation` | https://github.com/addyosmani/agent-skills | 为生产功能添加日志、指标、追踪和可诊断性。 |
| `obsidian-vault` | https://github.com/mattpocock/skills | 搜索、创建和整理 Obsidian vault 笔记和 wikilinks。 |
| `performance-optimization` | https://github.com/addyosmani/agent-skills | 分析和优化性能、Core Web Vitals、加载速度和瓶颈。 |
| `personal-skill-authoring` | local | 在这个个人 skills 仓库中新增、维护、适配和校验 Codex skills。 |
| `planning-and-task-breakdown` | https://github.com/addyosmani/agent-skills | 把明确规格拆成有顺序、可验证、可实现的小任务。 |
| `prototype` | https://github.com/mattpocock/skills | 做一次性原型，验证状态模型、业务逻辑或 UI 方向是否合理。 |
| `qa` | https://github.com/mattpocock/skills | 交互式 QA 会话，把用户反馈的问题整理成 GitHub issues。 |
| `request-refactor-plan` | https://github.com/mattpocock/skills | 通过访谈生成小步重构计划，并归档为 issue。 |
| `research` | https://github.com/mattpocock/skills | 针对技术问题查阅高可信来源，并把结果整理为 Markdown。 |
| `resolving-merge-conflicts` | https://github.com/mattpocock/skills | 处理正在进行的 merge 或 rebase 冲突。 |
| `scaffold-exercises` | https://github.com/mattpocock/skills | 创建课程练习目录、题目、答案和说明，并保证能通过 lint。 |
| `security-and-hardening` | https://github.com/addyosmani/agent-skills | 加固涉及用户输入、认证、存储、外部集成和会话的代码。 |
| `setup-matt-pocock-skills` | https://github.com/mattpocock/skills | 为 Matt Pocock skills 初始化 issue tracker、triage 标签和文档布局。 |
| `setup-pre-commit` | https://github.com/mattpocock/skills | 设置 Husky、lint-staged、格式化、类型检查和测试型 pre-commit。 |
| `shipping-and-launch` | https://github.com/addyosmani/agent-skills | 准备生产发布、发布前检查、灰度策略、监控和回滚方案。 |
| `source-driven-development` | https://github.com/addyosmani/agent-skills | 基于官方文档做实现决策，避免过时或未经证实的写法。 |
| `spec-driven-development` | https://github.com/addyosmani/agent-skills | 在开始新项目、功能或重大改动前先写规格。 |
| `tdd` | https://github.com/mattpocock/skills | 测试驱动开发，适合用户明确要求 red-green-refactor 或集成测试。 |
| `teach` | https://github.com/mattpocock/skills | 在当前 workspace 内教用户某个新技能或概念。 |
| `test-driven-development` | https://github.com/addyosmani/agent-skills | 针对功能、bug 和行为改动，用测试证明代码正确。 |
| `to-issues` | https://github.com/mattpocock/skills | 把计划、spec 或 PRD 拆成可独立领取的 issue。 |
| `to-prd` | https://github.com/mattpocock/skills | 把当前对话综合成 PRD 并发布到 issue tracker。 |
| `triage` | https://github.com/mattpocock/skills | 对 issues 和外部 PR 做分类、验证、追问和 agent-ready brief。 |
| `ubiquitous-language` | https://github.com/mattpocock/skills | 从对话中提取 DDD 统一语言术语表，标记歧义并建议标准术语。 |
| `using-agent-skills` | https://github.com/addyosmani/agent-skills | 发现并调用合适的 agent skills，适合会话开始或选择 workflow 时使用。 |
| `wayfinder` | https://github.com/mattpocock/skills | 把超大工作拆成调查 tickets，逐个解决直到路线清晰。 |
| `wizard` | https://github.com/mattpocock/skills | 生成交互式 bash 向导，引导人工完成第三方设置、迁移或状态切换。 |
| `writing-beats` | https://github.com/mattpocock/skills | 把原始材料组织成文章节拍和叙事路径。 |
| `writing-fragments` | https://github.com/mattpocock/skills | 挖掘和收集写作碎片，暂不强加结构。 |
| `writing-great-skills` | https://github.com/mattpocock/skills | 编写和编辑高质量 skills 的参考原则。 |
| `writing-shape` | https://github.com/mattpocock/skills | 把素材逐段塑造成完整文章。 |
