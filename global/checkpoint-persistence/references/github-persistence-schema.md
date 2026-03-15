# GitHub Persistence Schema

## 存储分层

### Issue 正文

Issue 正文用于保存当前可覆盖摘要，建议至少包含：

```md
# Task Summary

- Goal: ...
- Status: status:in-progress
- Stage: planning
- Next: ...
- Updated At: 2026-03-14 10:30 +08:00
- Key Paths:
  - agent-task-log/ongoing/2026-03-14-1_【plan】任务名称-实施计划.md
```

要求：

- 正文只保留当前状态，不承担历史追溯。
- 每次“存档”后，若摘要字段变化明显，应同步更新正文。

### Issue 评论

Issue 评论用于保存追加式历史记录。每条评论代表一个关键节点事件，不覆盖历史。

推荐 `kind`：

| kind | 触发时机 | 必含内容 |
|------|----------|----------|
| `checkpoint` | 阶段完成、暂停、继续前 | `Goal / Status / Next / Last Turn / Last Reply` |
| `plan` | 计划书首次创建或明显更新 | `Plan Path / Plan Snapshot / Next` |
| `reply` | 输出关键方案、结论、交接回复后 | `Last Reply / Last Turn / Next` |
| `decision` | 用户确认关键方案后 | `Decision / Constraint / Next` |
| `blocker` | 测试失败、依赖缺失、等待外部输入时 | `Blocker / Impact / Unblock Condition / Next` |
| `handoff` | 跨会话暂停、换 Agent、收尾前 | `Summary / Open Questions / Next / Last Reply` |

## 评论模板

```md
## Persistence Record

- Kind: checkpoint
- Timestamp: 2026-03-14 10:30 +08:00
- Stage: planning
- Status: status:in-progress
- Next: 更新 workflow 引用链
- Paths:
  - agent-task-log/ongoing/2026-03-14-1_【plan】任务名称-实施计划.md

### Goal

...

### Completed

...

### Blocker

...

### Decision

...

### Last Turn (verbatim)

User:
...

Agent:
...

### Last Reply Snapshot

<details>
<summary>展开最后一次回复</summary>

...

</details>

### Plan Snapshot

Path: agent-task-log/ongoing/2026-03-14-1_【plan】任务名称-实施计划.md

<details>
<summary>展开计划文档</summary>

...

</details>
```

要求：

- `Last Reply Snapshot` 与 `Plan Snapshot` 尽量保留原文，而不是只写摘要。
- 没有对应对象时，可省略对应章节；但 `Goal / Status / Next / Last Turn / Last Reply` 不得同时缺失。

## 大文本分段规则

当 `Last Reply` 或 `Plan Snapshot` 过长时，按以下规则处理：

1. 主评论保留摘要、时间戳、路径、`Next` 与分段索引。
2. 将正文拆为连续的附加评论，标题格式如下：

```md
## Persistence Attachment

- Kind: plan
- Part: 1/3
- Source Path: agent-task-log/ongoing/...

...
```

3. 拆分条件满足任一即可：
   - 单段超过 120 行
   - 单段超过 12000 字符
4. 禁止因为文本过长而只写“见本地文件”；若内容对恢复执行有价值，必须写入 GitHub。

## 读档提取优先级

恢复上下文时按以下顺序提取：

1. Issue 正文中的当前摘要
2. 最新 `handoff` 或 `checkpoint` 评论
3. 最新 `plan` 评论
4. 最新 `reply` 评论
5. 最新 `blocker` 或 `decision` 评论

若发现冲突：

- 以最新时间戳的评论为准
- 在读档输出中明确指出冲突字段，例如：`Status 冲突：正文=status:in-progress，最新评论=status:blocked`

## 最小读档输出

至少返回：

- `Issue #`
- `Status`
- `Stage`
- `Next`
- `Recent Kind`
- `Recent Plan Path`
- `Recent Blocker`
- `Recent Reply Summary`
