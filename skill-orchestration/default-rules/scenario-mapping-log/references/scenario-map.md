# 场景映射表 v0.6

> 这张表只维护“场景 -> 预期 skill”的映射关系。
> 运行中的命中比对格式见 [log-comparison-format.md](log-comparison-format.md)。
> 如果当前任务还没有稳定主场景，先不要强行套表。

## 1. 横切默认规则

- `human-steered-execution`
  适用于：除极简单步任务外的大多数协作执行任务
- `critical-thinking-evaluation`
  适用于：需要判断、比较、收敛、取舍的任务
- `source-quality-control`
  适用于：依赖外部资料、事实、API、产品信息或版本状态的任务
- `value-dense-delivery`
  适用于：需要压缩输出、提高价值密度的任务
- `readability-first-writing`
  适用于：需要优化说明、结构和阅读流的任务

## 2. 场景映射

### 2.1 coding/refactor

主问题：

- 在不破坏主线的前提下优化结构、降低复杂度、提高可维护性

Core:

- `architecture-governance`
- `single-responsibility`
- `core-first-simplicity`

Conditional:

- `file-guardrails`
- `critical-thinking-evaluation`
- `source-quality-control`
  适用于：涉及外部框架、API、版本迁移、第三方库行为判断
- `roi-value-density`
  适用于：用户明确在问“这次重构值不值得做”
- `python-coding-standards`
  适用于：当前改动落在 Python 实现层

Acceptable bypass:

- 直接进入 `architecture-governance + single-responsibility`
- 用户只要求做“是否值得重构”的判断，直接进入 `roi-value-density`

Typical gaps:

- 只做样式调整，没有解释结构性问题
- 没有说明当前改动为什么现在值得做
- 没有分析职责边界、依赖方向或影响范围

### 2.2 documentation/readme

主问题：

- 让首次读者快速理解项目是什么、怎么启动、核心价值是什么、结构如何组织

Core:

- `technical-readme-structure`

Conditional:

- `value-dense-delivery`
- `readability-first-writing`
- `critical-thinking-evaluation`
- `source-quality-control`
- `core-first-simplicity`
  适用于：README 信息过多、主线不清、需要收敛结构
- `roi-value-density`
  适用于：在多个 README 内容方向之间做取舍

Acceptable bypass:

- 用户只让补 README 结构，不涉及外部事实校验，直接进入 `technical-readme-structure`

Typical gaps:

- 只有目录框架，没有明确主线
- 缺少快速开始或一句话描述
- 包含较强事实性结论，却没有任何可信来源支撑

### 2.3 research/comparison

主问题：

- 收集并比较外部信息，在证据基础上形成判断或建议

Core:

- `source-quality-control`
- `critical-thinking-evaluation`

Conditional:

- `knowledge-synthesis`
- `value-dense-delivery`
- `readability-first-writing`
- `core-first-simplicity`
- `roi-value-density`
  适用于：比较之后需要给出“现在先做哪个”的建议
- `architecture-governance`
  适用于：比较对象是架构方案或系统设计路径

Acceptable bypass:

- 任务只是单纯做资料收集，不要求收敛决策，直接以 `source-quality-control` 为主

Typical gaps:

- 来源很多，但没有分级与主次
- 只有观点堆叠，没有证据与假设区分
- 结论力度过强，但证据级别偏低

### 2.4 decision/prioritization

主问题：

- 在多个候选动作之间判断哪个更值得当前推进

Core:

- `roi-value-density`
- `critical-thinking-evaluation`

Conditional:

- `core-first-simplicity`
- `value-dense-delivery`
- `readability-first-writing`
- `source-quality-control`
  适用于：判断依赖外部事实、版本状态、产品数据或市场信息
- `architecture-governance`
  适用于：决策对象是架构或模块边界调整

Acceptable bypass:

- 用户明确只做 ROI 与价值密度判断，直接进入 `roi-value-density`

Typical gaps:

- 只有泛泛建议，没有可比较候选
- 只说“值得做”，没有解释为什么现在做
- 没有说明主要风险与不确定性

### 2.5 python/setup-or-implementation

主问题：

- 在 Python 项目中处理环境、依赖、实现规范与工程基线

Core:

- `python-uv-acceleration`
  适用于：安装依赖、创建虚拟环境、替换 pip/venv
- `python-coding-standards`
  适用于：Python 代码实现、修改、补全

Conditional:

- `file-guardrails`
- `critical-thinking-evaluation`
- `source-quality-control`
  适用于：第三方库、API、版本行为判断
- `single-responsibility`
  适用于：当前改动涉及 Python 模块职责拆分
- `architecture-governance`
  适用于：当前问题已上升到架构与层级边界

Acceptable bypass:

- 用户只要求“把 pip 命令改成 uv”，直接进入 `python-uv-acceleration`
- 用户只要求“按 Python 规范修代码”，直接进入 `python-coding-standards`

Typical gaps:

- 仍然默认用 pip/venv，没有说明 uv 路径
- 写了 Python 代码，但没有类型、结构或日志基线
- 涉及外部库行为，却没有做来源验证

### 2.6 research/general-understanding

主问题：

- 为某个技术系统、框架、平台、工程主题或复杂产品能力建立高可信的宏观理解

Core:

- `general-understanding-research`
- `knowledge-synthesis`
- `source-quality-control`

Conditional:

- `critical-thinking-evaluation`
- `core-first-simplicity`
- `architecture-governance`
  适用于：目标对象包含明显架构层级、依赖关系、系统边界
- `technical-readme-structure`
  适用于：最终交付需落成技术入口型 README 或概览文档
- `roi-value-density`
  适用于：用户同时在问“先研究哪一块更值得”
- `practice-driven-learning`
  适用于：用户希望在建立理解之后继续通过实践、实验或小规模验证推进认知

Acceptable bypass:

- 用户只要求快速建立结构视角与演化视角，可直接进入 `general-understanding-research`

Typical gaps:

- 资料很多，但没有形成结构主线和演化主线
- 只罗列事实和来源，不解释为什么重要
- 没有区分事实、推断和开放问题

### 2.7 research/practice-and-learning-loop

主问题：

- 面对不确定任务时，通过“调查 -> 认识 -> 最小行动 -> 反馈 -> 修正”持续推进

Core:

- `practice-driven-learning`

Conditional:

- `critical-thinking-evaluation`
- `source-quality-control`
- `knowledge-synthesis`
  适用于：需要把多轮调查与反馈整理成研究笔记、复盘文档或学习文档
- `general-understanding-research`
  适用于：先要建立对象的结构视角与演化视角，再进入实践闭环
- `roi-value-density`
  适用于：要判断下一步最小行动先做哪个更值
- `architecture-governance`
  适用于：闭环验证对象是架构方案、模块边界或系统依赖设计

Acceptable bypass:

- 用户已经明确给出一个低风险、强针对性的最小验证动作时，可直接进入 `practice-driven-learning`

Typical gaps:

- 只有资料收集，没有下一步最小行动
- 只有行动计划，没有核心假设和反馈观测点
- 做了实践，但没有把结果回灌到当前认知

### 2.8 skill-system/design

主问题：

- 设计、重构、迁移或治理整个 skill 系统，使结构更清晰、更可维护、更可解释

Core:

- `agent-skill-rules`
- `scenario-mapping-log`

Conditional:

- `critical-thinking-evaluation`
- `core-first-simplicity`
- `roi-value-density`
  适用于：判断某个 skill 是否值得沉淀、是否应延后
- `source-quality-control`
  适用于：设计决策需要依赖外部平台规范或官方说明

Acceptable bypass:

- 用户只要求创建或重构单个 skill，直接进入 `agent-skill-rules`

Typical gaps:

- 只讨论命名，不讨论角色边界与治理方式
- 结构层级越来越多，但没有说明复杂度收益比
- 发现偏差后只归因“模型没命中”，不回看映射表和 skill 描述是否写偏

### 2.9 checkpoint/resume

主问题：

- 在跨会话、阶段切换、任务交接或长链路推进时，把关键上下文稳定存档，并在恢复时尽快回到可执行状态

Core:

- `github-checkpoint-persistence`

Conditional:

- `human-steered-execution`
- `value-dense-delivery`
- `critical-thinking-evaluation`
  适用于：需要判断哪些内容值得进 checkpoint，哪些只是噪音
- `scenario-mapping-log`
  适用于：要对照预期 skill 命中和实际推进链路一起做阶段复盘

Acceptable bypass:

- 任务极短、上下文极小且无需跨会话续接时，可不进入正式 checkpoint 流程

Typical gaps:

- 只保存结论，没有保存阻塞、风险和下一步
- 恢复时仍需重新翻大量对话，无法快速接续
- checkpoint 过长、过散，关键主线被噪音淹没
