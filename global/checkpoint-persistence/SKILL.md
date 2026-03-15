---
name: checkpoint-persistence
description: Agent 运行关键节点持久化与读档规则。用于将 checkpoint、最后一次回复、计划文档、关键决策、阻塞与下一步写入 GitHub Issues/Comments，并在新会话或阶段切换时恢复上下文。关键词：存档、读档、checkpoint、resume、日志、持久化、最后一次回复、计划书、GitHub、issue。
---

# Checkpoint Persistence

> 负责把任务执行过程中的关键节点沉淀到 GitHub，并在需要时读档恢复

## 核心强制要求

### 职责边界

- **负责**：关键节点存档、GitHub issue/comment 持久化、读档恢复、最后一次回复快照、计划文档快照、阻塞与下一步沉淀。
- **不负责**：主阶段路由、需求发现、计划拆解、测试执行、代码审查、任务关闭。
- issue 的创建或绑定可以由调用方完成；但执行“存档”且无可用 issue 时，允许本 skill 兜底创建 issue 并写入首条记录。

### 持久化对象

每次写入 GitHub 时，至少维护以下对象中的相关项：

| 对象 | 说明 | 是否必存 |
|------|------|----------|
| `summary` | 当前 `Goal / Status / Next / Stage / Updated At` | 是 |
| `last-turn` | 用户最后一次输入 + Agent 最后一次输出 | 是 |
| `last-reply` | Agent 最近一次实质性回复全文快照 | 是 |
| `plan-snapshot` | 最近一次计划文档内容与本地路径 | 有计划书时必存 |
| `decision` | 已确认的关键决策与约束 | 有则存 |
| `blocker` | 当前阻塞、影响范围、解除条件 | 有则存 |
| `handoff` | 交接说明、待续上下文、收尾前快照 | 需要交接时必存 |

### 必存字段

- `Goal`
- `Status`
- `Next`
- `Stage`
- `Updated At`
- `Last Turn`
- `Last Reply`
- `Issue #`

补充规则：

- 若本轮产生或更新了计划书、测试记录、诊断文档、收尾日志等本地 Markdown 文档，不能只记录路径，必须把最新正文或分段正文同步到 GitHub。
- 若本轮 Agent 已给出会影响后续执行的长回复、方案回复、审查结论或交接回复，必须将该回复原文快照存档到 GitHub。
- “存档”默认不是关闭任务；关闭 issue 仍由 `closure` 或显式收尾流程负责。

### 触发方式

- **手动触发**：用户说 `存档`、`读档`、`恢复进度`、`记录一下`、`把这个同步到 GitHub`。
- **自动触发**：出现以下关键节点时，调用方应主动执行本 skill：
  - 创建或绑定 Issue 后
  - 首次生成计划书，或计划书内容发生明显更新后
  - 阶段切换、CP 完成、进入测试、进入审查、进入收尾前
  - 出现 blocker、关键决策、验收结论后
  - 准备跨会话暂停、等待用户、交接给其他 Agent 前
  - 已输出实质性阶段总结，且任务后续仍会继续时

### GitHub 存储模型

- 一个长程任务对应一个 GitHub Issue。
- **Issue 正文**：保存可覆盖的摘要信息，例如 `Goal / Status / Next / Stage / Updated At / Key Paths`。
- **Issue 评论**：保存追加式事件日志，作为持久化主账本。
- 不允许只把上下文留在本地文件中；凡是后续恢复执行需要依赖的计划文档、最后一次回复、阻塞说明，都必须同步到 issue 评论。
- 标签沿用既有兼容方案：`status:*` + `type:*` + `repo:*` + `wf:*`。

### Issue 与仓库判定流程

1. 用户显式给出 `#issue` 或 `<owner>/<repo>`：直接使用。
2. 上下文已有绑定 `Issue #`：优先沿用。
3. 否则解析当前 Git 仓库远程，列出 open issue 候选。
4. 分支：
   - 候选 0 条且当前动作为“存档”：创建 issue 并写入首条持久化记录。
   - 候选 1 条：自动选中并告知用户。
   - 候选 2+ 条：列出最近更新的 3-5 条候选，等待用户选择。
   - 当前动作为“读档”且仓库仍不明确：先要求用户确认仓库，再继续。

### 两个标准动作

1. **存档（checkpoint / persist）**
   - 同步 issue 摘要字段：`Goal / Status / Next / Stage / Updated At`
   - 追加一条持久化评论，记录本轮关键进展
   - 写入 `Last Turn`
   - 写入 `Last Reply` 原文快照
   - 若计划文档存在且本轮新增或变更：写入 `Plan Path` 与 `Plan Snapshot`
   - 若存在 blocker / decision / handoff：写入对应章节

2. **读档（resume）**
   - 读取 issue 正文摘要和最近评论
   - 恢复：当前状态、下一步、最近阶段、最近计划文档路径、最近回复快照、最近 blocker 或 decision
   - 若摘要与最新评论冲突：以最新时间戳的评论为准，并在输出中提示冲突

### 命令参考

- 摘要同步：`gh issue edit <id> -R <owner>/<repo> --body-file <tmpfile>`
- 追加持久化记录：`gh issue comment <id> -R <owner>/<repo> --body-file <tmpfile>`
- 读档：`gh issue view <id> -R <owner>/<repo> --comments`
- 候选列表：`gh issue list -R <owner>/<repo> --state open --limit 20 --json number,title,updatedAt,labels,url`

评论结构、正文模板与大文本分段规则见 `references/github-persistence-schema.md`。

### 一行回执模板

- **存档回执**：`已存档 #<issue> | 类型:<kind> | 状态:<status> | 下一步:<next> | <url>`
- **读档回执**：`已读档 #<issue> | 状态:<status> | 下一步:<next> | 最近快照:<kind>@<time> | <url>`

字段规则：

- `kind` 推荐值：`checkpoint`、`plan`、`reply`、`decision`、`blocker`、`handoff`。
- `status` / `next` / `kind` 若缺失，使用 `-` 占位。
- 回执必须保持单行，便于快速扫读与复制。

## 边界情况

- `gh` 未登录：提示 `gh auth login`，停止写入。
- 仓库上下文不明确：先要求用户确认 `<owner>/<repo>`。
- 评论正文过长：按 `references/github-persistence-schema.md` 的分段规则拆成多条评论，但主评论必须保留摘要与索引。
- 仅有短句确认、无新增有效上下文时：可跳过写入，避免噪音评论；但若用户显式要求“存档”，仍应执行。
- 本地文档不存在但路径已被引用：在评论中显式标记 `artifact-missing`，不要伪造正文。

## 参考资料

- `references/github-persistence-schema.md` - GitHub issue 摘要模板、评论结构与大文本分段规则
