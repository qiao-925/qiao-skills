## qiao-skills

面向 Agent 的技能仓库，采用“按分组目录安装”的组织方式。

## npx 安装

### 按分组安装（推荐）

```bash
npx skills add https://github.com/qiao-925/qiao-skills/tree/main/agent-skill-rules
npx skills add https://github.com/qiao-925/qiao-skills/tree/main/agent-collaboration
npx skills add https://github.com/qiao-925/qiao-skills/tree/main/agent-workflow
npx skills add https://github.com/qiao-925/qiao-skills/tree/main/architecture-governance
npx skills add https://github.com/qiao-925/qiao-skills/tree/main/code-complexity-control
npx skills add https://github.com/qiao-925/qiao-skills/tree/main/language-engineering-python
npx skills add https://github.com/qiao-925/qiao-skills/tree/main/project-guide-assemble
npx skills add https://github.com/qiao-925/qiao-skills/tree/main/project-guide-cs-rag
npx skills add https://github.com/qiao-925/qiao-skills/tree/main/single-responsibility
```

### 说明

- 当前仓库以“分组目录”为主，每个分组目录下可包含 1 个或多个规则。
- `single-responsibility` 虽只有 1 条规则，也按目录方式安装即可。

## 规则分组总览

当前共 **9** 个分组、**21** 条规则。

### `agent-skill-rules`（1）

组说明：Skill 设计与治理的总规范，负责标准、结构与质量门禁。

- `agent-skill-rules`：Agent Skills 开放标准与治理规则。用于 skill 的创建、修改、重构、迁移、审计与维护，提供平台无关的结构标准、frontmatter 规范、渐进式披露与质量门禁。

### `agent-collaboration`（3）

组说明：Agent 协作通用规范，覆盖协作原则、思考引导与文档驱动开发。

- `ai-collaboration-principles`：AI 协作总原则，强调角色定位、系统性分析、风险评估、授人以渔与质量优先。
- `critical-thinking-guidance`：思考引导机制，先提引导问题再给答案，帮助用户保持主动思考。
- `doc-driven-development`：文档驱动开发规范，先查官方文档与示例再编码/修复，并遵循 MCP 调用规则（优先 Context7）。

### `agent-workflow`（6）

组说明：任务执行全流程工作流（W00-W05），覆盖读档、规划、测试、审查与收尾。

- `w00-workflow-checkpoint`：Workflow Checkpoint 基础能力（聚焦存档与读档），在 GitHub Issues 中记录进展并恢复上下文。
- `w01-requirement-discovery`：需求发现规范，通过角色扮演帮助用户在探索场景发现高 ROI 功能方向。
- `w02-task-planning`：复杂任务规划规范，覆盖需求决策、计划书创建与执行路径。
- `w03-testing-and-diagnostics`：测试与诊断工作流，包含单测/浏览器测与失败自动诊断。
- `w04-review-gate`：交付后审查门禁，提示新开 Agent 审查未提交代码后再收尾。
- `w05-task-closure`：任务收尾规范，包含日志生成与优化分析。

### `architecture-governance`（1）

组说明：通用架构与分层治理能力，面向跨项目复用与演进控制。

- `architecture-governance`：通用架构治理规范，提供分层约束、影响面分析、接口契约与依赖注入基线。

### `code-complexity-control`（4）

组说明：复杂度控制规范，强调简化、聚焦与可维护实现。

- `core-first-simplicity`：核心优先简化原则，融合 KISS 与“最小光辉点”做跨层级复杂度控制。
- `file-header-comments`：代码文件顶部注释规范，要求简洁说明文件用途与主要接口。
- `file-size-limit`：代码文件行数硬限制（≤300 行），超限必须拆分并先给方案。
- `project-principles`：兼容入口，已并入 `core-first-simplicity` 的 `project-level`。

### `language-engineering-python`（2）

组说明：Python 语言工程实践规范，覆盖编码标准与工具链加速。

- `python-coding-standards`：Python 编码规范，包括类型提示、日志规范、命名约定与代码结构。
- `python-uv-acceleration`：Python 生态加速规范，默认使用 `uv` 替代 `pip`/传统 `venv` 以提升效率。

### `project-guide-assemble`（2）

组说明：Assemble 项目定制技能，聚焦内容组织、提示词编排与整理产出。

- `prompt-recommendation`：Prompt 智能推荐与快速决策规则，适用于写作/优化/总结等任务。
- `whetstone`：批注式整理技能，将“原文 + 批注”整理为结构化笔记并生成 AI 总结。

### `project-guide-cs-rag`（1）

组说明：CS-RAG 项目专用架构规则入口，统一项目内架构认知与设计约束。

- `cs-rag-architecture-guideline`：CS-RAG 项目专用架构总规范，统一认知、设计与治理约束。

### `single-responsibility`（1）

组说明：单一职责专项规则，聚焦文件/函数/模块职责边界清晰化。

- `single-responsibility`：单一职责原则，确保文件、函数、模块职责清晰单一。

