---
name: working-memory-boost
description: 工作记忆持久化，在关键节点自动存档、跨 session 恢复上下文。自动触发条件——AI行为信号（最高优先级）：刚完成一批文件修改、执行完一个完整命令序列、输出了方案/设计/结论性长回复、本轮工具调用超过5次。用户确认信号：用户说"好"、"完成"、"done"、"行"、"下一步"、"接下来"后对话收尾；一个功能/模块被确认实现完毕；用户开始提出新的独立任务。语义信号：出现明确决策（"我们选择X"、"方案定了"）、重要洞察、架构选型、阻塞突破。手动信号："存档"、"checkpoint"、"读档"、"恢复"、"记录进度"、"同步"、"继续上次"、"工作记忆"、"跨设备"。
metadata:
  type: procedural
---

# Working Memory Boost

> 增强型工作记忆：双层备份架构，看板优先入口，自动完整性检查。跨 session 不丢失上下文。

工作记忆双层架构：本地 `.working-memory/` + 远程 GitHub Issue。

```
.working-memory/
├── board.md          # 全局看板（唯一入口）
├── ongoing/          # 进行中任务
├── archive/          # 按月归档
├── analysis/         # 数据分析（链接）
├── aha-moments/      # 顿悟记录（链接）
└── .checkpoint       # 机器状态
```

## Instructions

### Step 0：读取看板

所有操作必须先读取 `.working-memory/board.md`，向用户展示：
- 进行中任务列表
- 最近归档（前 3 个）
- 最新数据分析和 aha-moment 链接

### Step 1：确认动作

| 触发词 | 动作 |
|--------|------|
| 存档、记录、同步 | `checkpoint` |
| 读档、恢复、继续 | `resume` |

默认 `checkpoint`。

### Step 2：前置完整性检查（L1-L3）

**L1：board ↔ 文件自动同步**
- board 列出的任务，检查 `ongoing/*.md` 是否存在
- 文件存在但 board 未列：自动添加到 board「进行中」
- board 列但文件缺失：标记 `⚠️ 待重建`，尝试从 Issue 恢复
- 对比 mtime，新者胜，自动对齐

**L2：本地文件 vs .checkpoint**
- 读取 `.working-memory/.checkpoint`
- timestamp 不一致 → 询问用户：「本地文件较新 / checkpoint 较新 / 手动选择」

**L3：Git 状态**
- 检查 `HEAD` 是否与 `.checkpoint.git_ref` 一致
- 不一致 → 警告：「代码状态偏离 checkpoint 时的基线」

发现问题，询问用户后继续或修复。

### Step 3：执行动作

#### 存档（checkpoint）

流程：
1. 读取本地 `ongoing/任务名.md`
2. 更新 Checkpoint 状态表（用户或 AI 已更新）
3. 更新 `.checkpoint`：
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
4. 同步 `board.md`：更新该任务的「状态」「下一动作」「更新」列
5. 写入远程 Issue（正文 + 评论）

远程层极简：
- **Issue 正文**（5 行内）：
  ```
  优化 Embedding 缓存，减少 50% API 调用
  Status: 🔄 implementation
  Next: 实现 batch_get()
  Local: .working-memory/ongoing/2026-04-08-01_【plan】...
  Git: a1b2c3d
  ```
- **评论**：仅记录关键节点（CP 完成、阻塞、决策）

#### 读档（resume）

**判断模式：**
| 条件 | 模式 | 操作 |
|------|------|------|
| 本地文件存在且 mtime > 远程 | 热恢复 | 读取本地，验证 L3 |
| 本地文件缺失或 mtime < 远程 | 温恢复 | 从 Issue 重建本地 |
| 用户显式指定 `#issue` | 强制重建 | 从指定 Issue 重建 |

**温恢复流程：**
1. `gh issue view <id> --comments`
2. 解析 Issue 正文 + 最新评论
3. 重建 `ongoing/任务名.md`（精简三区块格式）
4. 重建 `.checkpoint`
5. 更新 `board.md`（如该任务未列出则添加）
6. 输出恢复摘要

### Step 4：后置完整性检查（L3）

- 再次验证 Git 状态
- 对比本次操作前后的 `.checkpoint` 变化
- 确认远程同步成功（可选：抽查 Issue 正文）

## 文档格式参考

**board.md（全局看板）：**
```markdown
# 工作记忆看板

## 进行中

| 任务 | 阶段 | 状态 | 下一动作 | 更新 |
|------|------|------|----------|------|
| [#42] 优化 Embedding | implementation | 🔄 | batch_get() | 04-08 |
| [#45] 重构 query | planning | ⬜ | 技术方案 | 04-08 |

## 最近归档

| 任务 | 结果 | 日期 |
|------|------|------|
| [#38] 配置模块 | ✅ | 04-07 |

## 数据分析

- [Bug 健康度](./analysis/README.md)

## Aha Moments

- [模型选择](../aha-moments/2026-01-22_模型选择的重要性.md)
```

**ongoing/*.md（单个任务）：**
```markdown
# 【plan】优化 Embedding 缓存

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


## 一行回执

**存档：**
```
已存档 #42 | implementation 🔄 | Next: batch_get()
本地: .working-memory/ongoing/...md ✅ | Git: a1b2c3d ✅
```

**读档（热）：**
```
已恢复 #42 | 来源:本地 | implementation 🔄 | Next: batch_get()
```

**读档（温）：**
```
已恢复 #42 | 来源:远程 | implementation 🔄 | Next: batch_get()
重建: .working-memory/ongoing/...md | Git: 一致
```

## Edge Cases

| 问题 | 策略 |
|------|------|
| `gh` 未登录 | 提示 `gh auth login`，停止 |
| L1 发现 board 与文件不一致 | **自动同步**，无需询问 |
| L2 timestamp 冲突 | 询问用户选择方向 |
| L3 Git 偏离 | 警告并显示差异 |
| 跨设备恢复时本地已有文件 | 比较 timestamp，新者胜，旧者备份 `.bak` |
| Issue 正文过长 | 压缩为 5 行内 |

## 参考资料

- `references/github-persistence-schema.md` - 远程层模板
- `references/working-memory-schema.md` - 本地层完整规范
