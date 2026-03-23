# GitHub Persistence Schema

## 1. 存储分层

### Issue 正文

Issue 正文保存“当前可覆盖摘要”，不承担历史追溯。建议至少包含：

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

- 每次存档后，若摘要字段变化明显，应同步更新 issue 正文。
- Issue 正文只保留当前状态，不保存完整历史。

### Issue 评论

Issue 评论保存追加式历史记录。每条评论代表一个关键节点事件。

推荐 `kind`：

| kind | 触发时机 | 必含内容 |
|------|----------|----------|
| `checkpoint` | 阶段完成、暂停、继续前 | `Goal / Status / Next / Progress Summary` |
| `plan` | 计划书首次创建或明显更新 | `Plan Path / Plan Summary / Next` |
| `reply` | 输出关键方案、结论、交接回复后 | `Reply Summary / Next` |
| `decision` | 用户确认关键方案后 | `Decision / Constraint / Next` |
| `blocker` | 测试失败、依赖缺失、等待外部输入时 | `Blocker / Impact / Unblock Condition / Next` |
| `handoff` | 跨会话暂停、换 Agent、收尾前 | `Summary / Open Questions / Next` |

## 2. 评论模板

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

### Reply Summary

...

### Plan

Path: agent-task-log/ongoing/2026-03-14-1_【plan】任务名称-实施计划.md

- Summary: ...
```

要求：

- 默认采用“路径 + 摘要”记录，不要求在评论中附上完整回复或计划书正文。
- 没有对应对象时，可省略章节；但 `Goal / Status / Next` 不得同时缺失。

## 3. 长文本处理原则

当 `Reply Summary`、`Plan Summary` 或其他记录内容过长时，按以下规则处理：

1. 先压缩为能支持恢复的简要摘要，保留 `Next`、关键结论与相关路径。
2. 默认不使用附件式评论，不要求追加 `Persistence Attachment` 分段。
3. 只有单条评论确实无法容纳最小必要信息时，才拆成少量连续评论，并保持同一 `kind` 与清晰索引。
4. 可以只写路径，但前提是同时补一段足以支持恢复的摘要；禁止只有“见本地文件”而没有任何上下文。

## 4. 读档提取优先级

恢复上下文时按以下顺序提取：

1. Issue 正文中的当前摘要
2. 最新 `handoff` 或 `checkpoint` 评论
3. 最新 `plan` 评论
4. 最新 `reply` 评论
5. 最新 `blocker` 或 `decision` 评论

若发现冲突：

- 以最新时间戳的评论为准
- 在读档输出中显式指出冲突字段

## 5. 最小读档输出

至少返回：

- `Issue #`
- `Status`
- `Stage`
- `Next`
- `Recent Kind`
- `Recent Plan Path`
- `Recent Blocker`
- `Recent Record Summary`
