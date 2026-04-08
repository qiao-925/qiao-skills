# Working Memory 本地层规范

## 目录结构

```
.working-memory/
├── board.md              # 全局看板（唯一入口）
├── ongoing/              # 进行中任务
│   └── YYYY-MM-DD-N_【type】任务名.md
├── archive/              # 按月归档
│   └── YYYY-MM/
│       └── YYYY-MM-DD-N_【type】任务名.md
├── analysis/             # 数据分析（链接或子模块）
│   └── README.md
├── aha-moments/          # 顿悟记录（链接或子模块）
│   └── README.md
└── .checkpoint           # 机器状态（隐藏 JSON）
```

## board.md（全局看板）

四区块结构：

```markdown
# 工作记忆看板

## 进行中

| 任务 | 阶段 | 状态 | 下一动作 | 更新 |
|------|------|------|----------|------|
| [#42] 优化 Embedding | implementation | 🔄 | batch_get() | 04-08 |

## 最近归档

| 任务 | 结果 | 日期 |
|------|------|------|
| [#38] 配置模块 | ✅ | 04-07 |

## 数据分析

- [Bug 健康度](./analysis/README.md)

## Aha Moments

- [模型选择](../aha-moments/2026-01-22_模型选择的重要性.md)
```

约束：
- 进行中 ≤5 行
- 归档 ≤3 行
- 数据分析和 aha-moments 只显示最新/摘要，以链接为主

## ongoing/*.md（单个任务）

三区块结构：

```markdown
# 【type】任务名称

> 一句话目标：减少 50% API 调用

## Checkpoint

| CP | 内容 | 状态 |
|----|------|------|
| 1 | 策略设计 | ✅ |
| 2 | core 实现 | 🔄 |
| 3 | 单元测试 | ⬜ |

## 当前上下文

- 决策：LRU + Redis 混合
- 阻塞：无
- 下一动作：实现 `batch_get()`

---
*Issue: #42 | Updated: 2026-04-08 14:30 | Git: a1b2c3d*
```

状态标记：
- ⬜ 待开始
- 🔄 进行中
- ✅ 已完成
- ⏸️ 暂停
- ❌ 取消

## .checkpoint（机器状态）

JSON 格式：

```json
{
  "issue": 42,
  "phase": "implementation",
  "completed": ["CP-1", "CP-2"],
  "next": "CP-3: 实现 core logic",
  "git_ref": "a1b2c3d",
  "timestamp": "2026-04-08T14:30:00Z"
}
```

字段说明：
- `issue`: 绑定的 GitHub Issue 编号
- `phase`: 当前阶段（planning/implementation/review/done）
- `completed`: 已完成的 CP 列表
- `next`: 下一动作描述
- `git_ref`: checkpoint 时的 Git commit
- `timestamp`: ISO 8601 格式

## 完整性检查 L1（自动同步）

规则：

| 场景 | 动作 |
|------|------|
| board 列出任务，文件存在 | 对比 mtime，新者更新对方 |
| board 列出任务，文件缺失 | 标记 `⚠️ 待重建`，尝试从 Issue 恢复 |
| 文件存在，board 未列 | 自动添加到 board「进行中」区块 |
| 多文件同名冲突 | 以最新 mtime 为准，旧者重命名 `.bak` |

## 归档规则

触发条件：
- 任务状态变为 `done` 或 `cancelled`
- 用户显式要求归档

操作：
1. 移动文件 `ongoing/*.md` → `archive/YYYY-MM/`
2. 更新 `board.md`：从「进行中」移除，添加到「最近归档」（保留最近 3 个）
3. 可选：关闭 GitHub Issue
