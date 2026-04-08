# GitHub Persistence Schema（远程层）

极简原则：Issue 正文 5 行内，评论仅记录关键节点。

## 1. Issue 正文（当前状态）

```
优化 Embedding 缓存，减少 50% API 调用
Status: 🔄 implementation
Next: 实现 batch_get()
Local: .working-memory/ongoing/2026-04-08-01_【plan】...
Git: a1b2c3d
```

约束：
- 仅 5 行：一句话目标 + Status + Next + Local 路径 + Git ref
- 每次存档后覆盖更新
- 不保留历史

## 2. Issue 评论（关键节点）

仅记录：CP 完成、阻塞出现、决策确认

```
CP-2 完成 | implementation 🔄

Completed:
- 缓存策略设计 ✅
- 接口定义 ✅

Next: 实现 batch_get()
```

## 3. 读档优先级

1. Issue 正文（当前状态）
2. 最新评论（CP 完成/阻塞/决策）

冲突解决：以时间戳新者为准。

## 4. 最小输出

- Issue #
- Status / Stage / Next
- Git ref
- Local path
