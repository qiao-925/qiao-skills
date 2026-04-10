---
name: skill-audit
description: 对指定 SKILL.md 进行静态审查。在修改任何 SKILL.md 后自动触发，或手动调用审计某个 skill。检查 frontmatter 规范、description 质量、正文结构与类型一致性、冗余内容。关键词：skill审查、skill-audit、审计、静态检查、frontmatter、description、类型一致性。
metadata:
  type: procedural
---

# Skill Audit

> 对 SKILL.md 进行静态审查，确保 skill 在推送前符合规范。审查标准以 `agent-skill-rules` 为准。

## Instructions

### Step 1：读取审查依据与目标

1. 调用 `@agent-skill-rules`，以其 Step 2（frontmatter）、Step 3（正文结构）、Step 4（自检清单）作为本次审查的标准
2. 读取被审查的 `SKILL.md` 全文

### Step 2：对照 agent-skill-rules 逐项检查

按 `agent-skill-rules` 的 Step 4 自检清单逐项核对，重点检查：

- `name` 与目录名一致，格式合规
- `description` 包含"做什么 + 何时触发 + 关键词"
- `metadata.type` 已声明（`procedural` / `declarative`）
- 正文结构与类型匹配（动作型用 Instructions，约束型用声明式）
- 无冗余章节，无平台绑定术语
- `SKILL.md` 与 `references/` 无重复维护

### Step 3：冗余与重复检查

- `description` 与正文是否重复维护同一内容
- 是否存在与执行无关的章节（更新日志、安装说明等）

### Step 4：输出审查报告

格式：

```
## Skill Audit Report：[skill-name]

**结论**：✅ 通过 / ⚠️ 需要调整

### 检查结果

| 检查项 | 状态 | 说明 |
|--------|------|------|
| frontmatter 完整性 | ✅/❌ | |
| description 触发条件 | ✅/❌ | |
| description 关键词 | ✅/❌ | |
| 类型一致性 | ✅/❌ | |
| 无冗余内容 | ✅/❌ | |

### 问题清单（如有）

1. [具体问题描述 + 建议修改方式]
```

若有问题，输出清单后等待修复，不继续推送。

## Edge Cases

| 情况 | 处理 |
|------|------|
| 目标 skill 不存在 | 报错，停止 |
| 只修改了 `references/` 或文档 | 跳过审查 |
| `metadata.type` 缺失 | 标记为问题，提示补充 |
