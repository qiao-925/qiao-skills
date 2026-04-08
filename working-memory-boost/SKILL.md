---
name: working-memory-boost
description: 增强型工作记忆。双层备份（本地 .working-memory/ + 远程 GitHub Issue）+ 全局看板 + 自动完整性检查。核心设计：看板优先、言简意赅、前后校验。关键词：工作记忆、checkpoint、resume、board、跨设备、双层备份、完整性检查、增强。
metadata:
  type: procedural
---

# Working Memory Boost

> 增强型工作记忆：双层备份架构，看板优先入口，自动完整性检查。

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

## 核心原则

1. **看板优先**：任何操作先看 `board.md`
2. **言简意赅**：一句话目标，5 行内状态
3. **自动同步**：L1 完整性检查自动对齐 board 与文件
4. **前后校验**：存档/读档前后都执行三层检查

## 负责与不负责

### 负责

- 维护 `.working-memory/board.md` 全局看板
- 维护 `.working-memory/ongoing/*.md` 任务文档
- 自动 L1 同步（board ↔ 文件）
- 存档：本地 → 远程
- 读档：本地优先，缺失则从远程重建
- 三层完整性检查（前后执行）

### 不负责

- 需求分析与任务创建
- 代码实现与测试
- 代码审查
- 任务关闭决策

## 何时使用

### 触发词

**存档（checkpoint）：**
- "存档"、"记录进度"、"同步"
- 阶段完成时自动调用

**读档（resume）：**
- "读档"、"恢复"、"继续"
- "从 #xx 恢复"、"跨设备恢复"

### 使用流程

1. 任何操作先读取 `board.md`
2. 用户指定任务或确认当前任务
3. 执行存档或读档
4. 前后自动完整性检查

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

### 本地文档格式

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
