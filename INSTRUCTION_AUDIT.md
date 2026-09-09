# GPT-6 Astra 指令精简记录

## 依据

本次通过搜索定位并完整读取以下两份网页正文，而非仅依据搜索摘要：

- [OpenAI Model Guidance — Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model)：重点为 Initiative and follow-through、Instruction following、Subagent delegation、Testing and verification。
- [Eric Provencher — Rethinking skills and prompts for GPT-6 Astra](https://x.com/pvncher/status/2095991462416490862)：重点为短而准确的技能描述、渐进披露、删除通用流程脚手架、明确授权与完成边界。

官方建议是按场景校准，不是禁止测试、提问或委派。本次没有套用所有官方示例提示词，也没有调整模型、推理强度或运行时参数。下面记录的是审计判断，不是已完成的模型性能基准。

## 生效范围

- 检查时，仅仓库根 `AGENTS.md` 属于已发现的项目/祖先/全局上下文文件；未发现额外 `CLAUDE.md`、`AGENTS.override.md`、`SYSTEM.md` 或 `APPEND_SYSTEM.md`。
- 完整检查了 7 个个人 `SKILL.md` 及其 `agents/openai.yaml`、清单选中的 55 个上游 `SKILL.md`，并按需查看相关引用。原默认安装数 62，调整后 45；其中手动调用技能不等于自动加载的描述数量。
- 本机个人和上游技能通过 `~/.pi/agent/skills/` 中的软链接指向仓库。个人文件修改随链接可见；筛选项由安装器同步后移除受管软链接。运行中的提示词仍需 `/reload` 或新会话刷新。
- `SKILLS.md` 是生成目录，不是全量自动注入的指令。技能描述在发现阶段加载，技能正文按需读取；`agents/openai.yaml` 是其他兼容工具的 UI 元数据。

## 已修改

| 位置 | 调整及理由 |
| --- | --- |
| `AGENTS.md` | 从 99 行缩为 25 行。删除泛化编码格言、遇不确定就停、默认访谈/计划/验收测验；改为完成已授权工作，仅澄清影响结果的决策。验证命令按变更类型触发。 |
| `skills/find-unknowns/SKILL.md` | 删除固定阶段、冗长技能接力表、强制产物链与“小任务也做测验”；保留针对真实未知的扫描、原型、问题和研究工具箱。 |
| `skills/minimal-diff/SKILL.md` | 删除固定行数/文件数阈值、模板化汇报和把配置/API 一概列为审批区；保留范围、用户改动保护与回退风险检查。 |
| `skills/personal-skill-authoring/` | 合并重复写作流程，强调窄触发、按需资料和结果边界；同步清理 Codex 专属措辞。 |
| 学术技能 | 缩短描述；审稿细项移至 `academic-peer-review/references/review-lenses.md`，完整审稿时读取；快速引用检查不再默认触发完整综述流程，不重复查询已核实记录。 |
| `skills/b200-pod/SKILL.md` | 明确用户指定运行/传输请求可构成该范围内的授权，避免逐条再确认；保留敏感覆盖/删除确认、令牌保护和共享 GPU 隔离。 |
| `scripts/install-skills.py` | 筛选暴露了“来源全部被排除即误判未初始化”的问题。初始化检查在应用排除前检查来源，仍阻止缺失或空来源触发部分安装/清理；用临时目录回归测试验证。 |

## 默认排除的 17 项

通过 `skill-sources.json` 排除，未修改或删除上游源码；需要时可恢复选择。

- 通用流程：`context-engineering`、`git-workflow-and-versioning`、`incremental-implementation`、`spec-driven-development`、`planning-and-task-breakdown`、`interview-me`、`karpathy-guidelines`。原描述包含“新会话”“每次代码变更”“超过一个文件”等宽触发，正文叠加计划审批、自动提交、重复澄清等要求。
- 测试/审查重复：`test-driven-development`、`code-review-and-quality`、`debugging-and-error-recovery`、`code-simplification`、`documentation-and-adrs`。例如全套测试作为每次完成条件、每个简化步骤运行测试集，以及任意错误都走固定六阶段。TDD 原文已有“不重复运行未变代码测试”的规则，问题主要是范围和触发频率。
- 固定研究/委派：`source-driven-development`（每个框架决策必须查官方资料）、`doubt-driven-development`（普通分支逻辑也触发独立评审）、`research`（必须后台代理及落盘报告）、`code-review`（固定双代理且不能合并排序结果）。模型仍可按任务需要研究和审查。
- 重复浏览器流程：`browser-testing-with-devtools` 默认要求每次浏览器改动都做广泛 QA，并对复现点击再询问。保留 `webapp-testing` 和前端技能，浏览器验证能力仍在。

保留专业文档格式、学术证据、图形重建、性能测量、安全、部署、迁移等技能。其工具陷阱、真实性要求和生产边界并未因模型变强而失效。`grilling`、`doc-coauthoring` 等有明确交互目的的工作流也未按普通编码流程一刀切删除。

## 后续上游更新

2026-09-09 更新上游版本时，继续排除了 5 个新出现但不符合当前筛选策略的技能：`academy-guide`（Claude 专属且触发过宽）、`discernment-nudge`（对多数实质回答追加固定追问）、`constraint-driven-development`（缺少质量基线时默认启动访谈和流程）、`implement-spec`（与已排除的实施编排流程重复）及 `retro`（仍位于上游 `in-progress`，且依赖特定会话日志与 review 工作流）。其余已选技能更新到新的固定子模块版本。

## 其他持久化指令与限制

以下来自安装包或仓库外配置，本次未覆盖、篡改或通过禁用整个工具来规避：

- Pi 核心仍要求 Pi 主题的 Markdown 完整阅读及追踪相关文档；只有广泛替换系统提示词才能移除此要求，不值得为本次精简重写核心提示词。
- `pi-web-access` 重复建议 2–4 个查询；单查询仍受支持，但未找到独立的提示词措辞配置。
- `@tintinweb/pi-subagents` 仍注入广泛探索委派建议。compact 模式只缩短工具描述，不能删除独立的硬编码指导。当前仓库安装器也不支持同步该包的顶层自定义代理配置；未为此扩展安装架构。
- plan/goal 包的计划和验证循环是条件激活的工作流，未将它们误当成每个会话都生效的规则。包提供的 `mcp-scripting` 保留工具协议指导。
- 仓库外 `~/.agents/skills/find-skills/SKILL.md` 仍有“how do I do X”宽触发及排行榜优先搜索流程，不在本仓库管理范围，未修改。
- 保留的上游专业技能仍有个别强流程要求，例如固定前端断点、合并冲突技能的自动提交、设计分支的多代理探索。这不是所有上游内容都已完全适配的声明；进一步修改应采用有明确需求的个人变体，而非直接改子模块。

未读取或提交凭证、会话或信任记录。原有未跟踪的 `external/supervisor-skills/` 保持原样。未做模型耗时或 Token 基准，因此不声称实际节省比例。
