# Skills 触发清单

本清单针对本仓库 `skill-sources.json` 选出的技能，不包含另行安装的 Pi 包或其他目录中的技能。完整能力目录见 [SKILLS.md](SKILLS.md)。

## 必须显式触发：8 个

以下技能的 `SKILL.md` 配置了 `disable-model-invocation: true`。Pi 不会把它们的描述放进自动匹配列表；需要使用 `/skill:<name>`。只描述任务不保证加载，想确保使用请直接输入命令。

| 技能 | Pi 命令 | 主要用途 |
| --- | --- | --- |
| blast-radius | `/skill:blast-radius 检查当前 diff 的隐性影响` | 追踪跨模块、依赖和数据契约风险，验证关键安全假设；默认只审查、不修复 |
| grill-with-docs | `/skill:grill-with-docs 梳理这个设计` | 深挖设计问题，同时记录术语表和架构决策 |
| wayfinder | `/skill:wayfinder 规划这个跨会话任务` | 把大任务整理成决策地图与待解决问题；涉及 issue tracker 时仍遵守外部操作授权边界 |
| writing-fragments | `/skill:writing-fragments 收集这篇文章的素材` | 通过访谈积累写作片段，暂不安排结构 |
| writing-beats | `/skill:writing-beats 根据素材逐个推进叙事节点` | 每轮选择下一段叙事方向，再逐步写入文章 |
| writing-shape | `/skill:writing-shape 把素材整理成文章` | 从原始材料出发，协作确定文章结构并逐段成文 |
| handoff | `/skill:handoff 下一轮继续处理安装器更新` | 把当前会话压缩为临时交接文档，便于新会话接续 |
| teach | `/skill:teach 教我理解这个模块` | 建立有学习记录、资料和课程的持续教学工作区，并非简单解释代码 |

`writing-*` 三个技能来自上游 `in-progress/`，属于实验性工作流。其他宿主的命令形式可能不同；这里的 `/skill:` 写法专用于 Pi。

## 需要表达意愿，但不必输入命令

- **grilling**：明确要求“拷问这个方案”“深挖我的假设”等即可匹配；普通实现任务不应自动变成连环访谈。
- **doc-coauthoring**：文档任务可以自动匹配并提出结构化协作方式；用户接受后才进入该流程，拒绝则自由协作。

这两项没有设置硬性的手动专用字段。它们与上表的“必须输入显式命令”不同。

## 其余技能

本次更新后的权威安装集合为 **57 个技能：8 个手动专用，49 个可按任务自动匹配**。自动匹配不代表每次都一定加载；要确保使用某个技能，所有技能都可以显式输入 `/skill:<name>`。

例如：论文写作匹配 `academic-writing`，PDF 处理匹配 `pdf`，调试匹配 `diagnosing-bugs`，去 AI 文风匹配 `humanizer`。`theme-factory` 的主题确认、`goutoujunshi` 的长期记忆同意等属于具体动作的确认要求，不等于整个技能必须手动触发。

## 更新后重新核对

升级上游后，重新检查手动专用字段以及描述和正文中的 opt-in 约定；仅靠关键词搜索不能确定流程是否需要用户同意。以下命令复用安装器的权威选择和字段判断，打印硬性手动清单：

```bash
python3 -B - <<'PY'
from pathlib import Path
import runpy
m = runpy.run_path('scripts/install-skills.py')
skills, warnings = m['discover_all'](Path.cwd())
manual = [s for s in skills if m['is_manual_only'](s)]
print(f'total={len(skills)}, manual={len(manual)}')
for s in manual:
    print(f'/skill:{s.name}  {s.path.relative_to(Path.cwd())}/SKILL.md')
for warning in warnings:
    print('WARNING:', warning)
PY
```

安装器以目录名安装技能；AI 基建来源中的目录 `model-pr-optimization-history` 在上游 frontmatter 声明为 `model-pr-history-knowledge`，存在命名差异。该技能没有硬性手动标记，使用时以 Pi 实际发现的命令为准。

安装后的当前 Pi 会话需要 `/reload` 或重启才能重新发现技能；仓库清单与尚未重载的会话列表可能不同。
