---
name: doc-driven-development
description: 文档驱动开发规范，要求 Agent 在生成代码或修复 bug 前先查阅官方文档与示例，包含 API 验证流程和搜索策略。适用于接入第三方库、排查 API 报错、版本变更等场景。
---

# 文档驱动开发规范

> 在生成代码或修复 bug 时，先看官方文档与示例，再动手实现。

---

## ⚠️ 核心强制要求

### 必须查文档的场景

- 落地新功能、接第三方库 API、或排查 API 报错时，**先查官方文档**
- 遇到 `AttributeError` / `TypeError` / 版本变更不确定时，**必须验证 API 定义与示例**
- 对项目自带封装的内部 API，可酌情跳过

### Agent 执行步骤

1. **停止猜测**：明确要查的 API/模块名称和版本
2. **查阅文档**：优先使用 `use context7` 抓取官方文档；若 MCP 不可用，改用 Firecrawl 抓取
3. **基于文档实现**：依据文档的参数、返回值和示例实现或修复代码

---

## AI Agent 行为要求

### 问题识别

| 问题类型 | 特征 | 处理方式 |
|----------|------|----------|
| API 不存在 | `AttributeError: 'X' has no attribute 'Y'` | 查找正确的 API |
| 参数错误 | `TypeError: unexpected keyword argument` | 查找正确的参数 |
| 行为异常 | 结果不符合预期 | 查找正确的用法 |
| 版本问题 | 某版本后 API 变更 | 查找版本差异 |

### 收集错误信息

必须收集：
- 完整的错误堆栈
- 相关代码片段
- 使用的库/框架版本

### 基于文档实现（禁止猜测）

```python
# 错误：基于猜测实现
index.query(question, top_k=10)  # 可能参数名不对

# 正确：基于文档实现
# 查阅文档后确认正确的参数名
index.query(question, similarity_top_k=10)
```

### 修复后验证

- [ ] 运行测试确认修复
- [ ] 检查是否引入新问题
- [ ] 验证在不同场景下的表现

---

## 参考资料

- `references/api-verification.md` - API 验证流程详细说明（问题识别、文档查阅、实施修复）
- `references/search-strategy.md` - 文档搜索策略与提问指引
