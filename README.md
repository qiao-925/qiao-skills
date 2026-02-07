Skills 功能清单（按目录名排序）

# 通用规则

## 架构，系统设计，程序设计
architecture-governance: 通用架构治理规范；抽象分层约束、影响面分析、接口契约、依赖注入与可插拔设计，适用于跨项目复用。
single-responsibility: 单一职责原则；保证文件/函数/模块职责清晰，避免循环依赖；可独立使用，也可由 architecture-governance 联动触发。

## 工作流
requirement-discovery: 需求发现；在迷茫/探索场景用角色扮演+ROI 评估产出高 ROI 方向（对话式输出，不生成文档）。
cross-agent-review: 交付完成且存在 git 未提交变更时，提示“新开 Agent 做代码审查”，审查通过后再收尾。
task-closure: 收尾流程；结构检查通过后生成任务日志与六维度复盘分析；含 generate_task_log.py。
task-planning: 任务规划；复杂任务（>=3 步）生成计划书/Checkpoint/决策点/文件清单；含 generate_task_plan.py。
testing-and-diagnostics: 正式测试与诊断；先建 TEST 记录文档，再按变更跑单测/浏览器测；失败进入最多三轮诊断；含 run_test_workflow.py/run_browser_tests.py/auto_diagnose.py。

task-checkpoint

## 文件，文档规则
documentation-standards: Markdown 文档规范（标题编号、日期格式、引用/代码块规范、篇幅控制与提交前检查）。
file-header-comments: 代码文件顶部注释规范；要求用简短注释说明文件用途/主要接口/可选示例，避免长篇流程描述。
file-operations: 文件操作门禁；任何新建/修改/删除前必须“授权→变更预览→确认”；重命名含 emoji 的目录优先用 Python 脚本处理。
file-size-limit: 硬限制：单个代码文件必须 <= 300 行；超限必须拆分并先给拆分方案。
folder-naming: 文件夹命名规范（图标+名称+统计信息）；用于新建/重命名知识库目录或做目录统计命名。

## 项目规则
project-principles: 项目聚焦原则；围绕“最小光辉点”，砍掉偏离核心的需求，避免过度设计，允许临时方案。

## 一般编码规则

## python
python-coding-standards: Python 代码规范；强制类型标注、日志规范（禁用 print）、命名与结构基线等。

# 项目定制规则

## assemble skills
prompt-recommendation: Prompt 智能推荐；根据任务类型推荐 1–3 个 Prompt 并给执行步骤（用于写作/优化/总结/组织内容等）。
whetstone: 批注式整理；把“原文+你的批注”整理成“编号批注+对应原文片段”，并输出 AI 总结（触发词：磨刀石/批注式整理等）。


## 项目专用架构规则
cs-rag-architecture-guideline: 【项目主入口】CS-RAG 项目架构总规范；已无损承载 cognition+design 全量内容，按“认知→设计→复核”执行。