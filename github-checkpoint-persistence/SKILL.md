---
name: github-checkpoint-persistence
description: GitHub 专用的 checkpoint 持久化与读档 skill。用于把任务关键节点、最近进展摘要、计划文档路径、关键决策与阻塞写入 GitHub issue/comment，并在跨会话、阶段切换、交接或恢复进度时从 issue 恢复上下文。关键词：GitHub、checkpoint、persist、resume、issue、comment、gh、存档、读档、handoff。
metadata:
  type: procedural
---

# GitHub Checkpoint Persistence

使用 GitHub Issue/Comment 作为长任务的外部记忆账本。

这个 skill 是 GitHub 专用流程能力，不是通用持久化抽象。它默认依赖：

- GitHub 仓库上下文
- `gh` CLI
- 当前任务需要跨会话、跨阶段或交接恢复

## 负责与不负责

负责：

- 关键节点存档
- 最近一次关键进展摘要
- 计划文档路径或简要摘要
- blocker / decision / handoff 持久化
- 从 GitHub issue 恢复上下文

不负责：

- 需求发现
- 主阶段路由
- 测试执行
- 代码审查
- 任务关闭

## 何时使用

- 生成计划书后自动触发存档，存档计划书这一关键节点
- 用户手动输入，存档，读档时触发

以下情况适合触发本 skill：

- 用户明确说“存档”“读档”“恢复进度”“同步到 GitHub”
- 长任务准备暂停、跨会话续做、交接给其他 Agent
- 首次生成或明显更新计划书后
- 出现 blocker、关键决策、阶段切换或阶段性总结后

## Instructions

### Step 1：确认动作类型

先判断当前是：

- `persist`：把最新上下文写入 GitHub
- `resume`：从 GitHub 恢复上下文

若用户没有显式说清，但包含“存档 / 记录 / 同步”语义，按 `persist` 处理。  
若包含“读档 / 恢复 / 继续上次进度”语义，按 `resume` 处理。

### Step 2：确认仓库与 issue

按以下顺序定位目标 issue：

1. 用户显式给出 `#issue` 或 `<owner>/<repo>`：直接使用。
2. 上下文已有绑定 `Issue #`：优先沿用。
3. 否则解析当前 Git 仓库远程并查询 open issues。

分支规则：

- `persist` 且候选为 0：允许创建 issue 后继续写入。
- 候选为 1：自动选中并告知用户。
- 候选大于 1：列出最近更新候选，等待用户确认。
- `resume` 且仓库或 issue 仍不明确：先要求用户确认，再继续。

### Step 3：执行 persist

执行存档时，默认只维护两层结构：

1. Issue 正文中的 `Task Summary`
2. Issue 评论中的 `Persistence Record`

`Task Summary` 至少包含：

- `Goal`
- `Status`
- `Stage`
- `Next`
- `Updated At`
- `Issue #`

有则追加：

- `Key Paths`

`Persistence Record` 至少包含：

- `Kind`
- `Timestamp`
- `Stage`
- `Status`
- `Next`

有则追加：

- `Completed`
- `Decision`
- `Blocker`
- `Handoff`
- `Plan Path`
- `Reply Summary`

执行顺序：

1. 更新 issue 正文中的当前摘要。
2. 追加一条持久化评论，记录本轮关键进展。
3. 若本轮涉及计划书、关键结论或交接内容，默认记录路径加简要摘要，不要求把全文作为附件写入评论。

默认优先“路径 + 摘要”，而不是“路径 + 全文快照”。只有原文无法稳定访问且缺少摘录会影响恢复时，才补最小必要片段。

### Step 4：执行 resume

读档时，至少恢复以下内容：

- 当前 `Status`
- 当前 `Stage`
- 当前 `Next`
- 最近一次 `Kind`
- 最近 `Key Paths / Plan Path`
- 最近 blocker / decision
- 最近一条 record 摘要

恢复顺序默认参考 `references/github-persistence-schema.md`。

若 issue 正文摘要与最新评论冲突：

- 以最新时间戳的评论为准
- 在输出中显式指出冲突字段

### Step 5：使用 GitHub 命令

常用命令如下：

- 摘要同步：`gh issue edit <id> -R <owner>/<repo> --body-file <tmpfile>`
- 追加记录：`gh issue comment <id> -R <owner>/<repo> --body-file <tmpfile>`
- 读档：`gh issue view <id> -R <owner>/<repo> --comments`
- 列候选：`gh issue list -R <owner>/<repo> --state open --limit 20 --json number,title,updatedAt,labels,url`

正文模板与读档优先级见：

- `references/github-persistence-schema.md`

## Examples

### Persist 触发

- `存档`
- `把这个同步到 GitHub`
- `记录一下当前进度`

### Resume 触发

- `读档`
- `恢复进度`
- `继续上次那个 issue`

## Edge Cases

- `gh` 未登录：提示 `gh auth login`，停止写入。
- 仓库上下文不明确：先确认 `<owner>/<repo>`。
- 评论正文过长：先压缩为摘要并保留关键路径；仅在确有必要时拆成少量连续评论，不使用附件式展开模板。
- 没有新增有效上下文：可跳过噪音写入；但若用户显式要求“存档”，仍应执行。
- 本地文档缺失：显式标记路径不可用或 `artifact-missing`，不要伪造正文。

## 一行回执模板

- `persist`：`已存档 #<issue> | 类型:<kind> | 状态:<status> | 下一步:<next> | <url>`
- `resume`：`已读档 #<issue> | 状态:<status> | 下一步:<next> | 最近记录:<kind>@<time> | <url>`

## 参考资料

- `references/github-persistence-schema.md` - GitHub issue 摘要模板、评论结构、长文本处理原则与读档优先级
