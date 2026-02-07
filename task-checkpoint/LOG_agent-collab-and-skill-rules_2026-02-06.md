## 背景
- 会话时间：2026-02-06 19:31:34
- 诉求概述：完善 skill 体系（重点为 agent-skill-rules 与 Agent 协作四个 skill 的合并/聚合方案），并保证迁移过程不失真。

## 主题拆分
### 1）agent-skill-rules 建设
- 讨论内容：将 create/management 能力整合为统一规则型 skill，并保持平台无关（去除 Cloud/IDE 绑定）。
- 结论：完成 `agent-skill-rules` 重构，明确官方 Step1-4 为主流程，并新增来源说明与增强规则。

### 2）无损迁移原则
- 讨论内容：用户指出此前合并有“失真与细节丢失”问题，要求禁止过度摘要。
- 结论：已将“无损迁移”写入 `agent-skill-rules/SKILL.md`（migrate/merge 强制），并补充校验与反模式条款。

### 3）Agent 协作 skill 聚合
- 讨论内容：将 `ai-collaboration-core`、`think-before-answer`、`doc-driven-development`、`concise-communication` 聚合为统一入口，同时保留细节。
- 结论：建立 `agent-collaboration-suite` 作为聚合入口；采用“导航层 + 原文层”结构；删除摘要化替代文件，保留 `references/original/*` 全量原文。

## 关键结论
- 规则层：`agent-skill-rules` 已明确“无损迁移”是 merge/migrate 强制要求。
- 协作层：`agent-collaboration-suite` 可作为主入口，原始细节保留且可追溯。
- 风险层：若后续清理旧入口，触发一致性会更稳定；当前主要负担不在体量，而在入口治理。

## 后续动作
- 决定是否下线/归档旧四个 Agent 协作入口（避免双轨维护）。
- 若保留旧入口，需声明与 suite 的主从关系和同步机制。
- 继续后续 skill 治理任务时，优先按 `agent-skill-rules` 的无损迁移流程执行。
