---
description: Prompt智能推荐系统快速决策规则（完整文档见系统文档）
alwaysApply: true
globs: []
---

# 智能决策机制

> 📖 **完整文档**：详见 `# 🎯 prompt-toolkit (18个文件，2.8%)/🤖 Prompt智能决策与编排系统.md`  
> ⚡ **快速参考**：此文件为AI自动加载的快速决策规则，包含13个Prompt文件路径映射和按需引用机制

## 🚨 核心指令（必须严格执行）

**当用户提出需求时，立即执行以下流程，不得跳过：**

## 🧠 核心决策流程

1. **分析任务类型**：创作？优化？验证？整理？
2. **推荐1-3个Prompt**（保持注意力集中）
3. **给出执行建议**：清晰的步骤和理由

## 🎯 快速匹配规则

| 用户需求 | 推荐Prompt |
|---------|-----------|
| "写技术文章" | 技术内容思路构建Prompt |
| "文字太枯燥" | 可读性优化Prompt |
| "分析这个方案" | **综合批判性分析Prompt（必选）** |
| "总结对话" | 深度对话总结专家Prompt |
| "生成README" | README生成和更新Prompt |

## 🚨 核心原则

- ✅ **最多推荐3个Prompt**（避免注意力分散）
- ✅ **重要决策必须批判性分析**（技术方案/架构设计/技术选型）
- ❌ 不要推荐相互冲突的Prompt
- ❌ 不要忽视任务的实际阶段

## 📚 13个Prompt库文件路径映射

### 📝 内容创作类
- **技术内容思路构建Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/技术内容思路构建Promot.md`
- **案例文章整理与优化Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/案例文章整理与优化Prompt.md`
- **深度对话总结专家Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/深度对话总结专家Prompt.md`
- **README生成和更新Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/README生成和更新Prompt.md`
- **报告类内容组织Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/报告类内容组织Prompt.md`

### 🎨 格式优化类
- **可读性优化Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/可读性优化Prompt.md`
- **Markdown图标美化Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/Markdown图标美化Prompt.md`

### 🔍 质量保证类
- **综合批判性分析Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/综合批判性分析Prompt.md`
- **数据来源验证Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/数据来源验证Prompt.md`
- **立场客观性警告Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/立场客观性警告Prompt.md`

### 🤝 协作优化类
- **人机共创精简价值Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/人机共创精简价值Prompt.md`
- **可复用Prompt识别与生成专家Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/可复用Prompt识别与生成专家Prompt.md`

### 🛠️ 工具辅助类
- **目录结构统计与排序Prompt** → `# 🎯 prompt-toolkit (18个文件，2.8%)/目录结构统计与排序Prompt.md`

## 🔧 按需引用机制

### 推荐后的执行流程

当推荐Prompt后，AI应：

1. **自动@引用**：使用 `@# 🎯 prompt-toolkit (18个文件，2.8%)/[文件名].md` 格式直接引用对应Prompt文件
2. **执行Prompt**：读取并执行对应Prompt的内容
3. **组合执行**：如果推荐多个Prompt，按顺序依次@引用和执行

### 引用格式示例

```
推荐：可读性优化Prompt
→ AI自动执行：@# 🎯 prompt-toolkit (18个文件，2.8%)/可读性优化Prompt.md

推荐：技术内容思路构建 + 可读性优化
→ AI依次执行：
   1. @# 🎯 prompt-toolkit (18个文件，2.8%)/技术内容思路构建Promot.md
   2. @# 🎯 prompt-toolkit (18个文件，2.8%)/可读性优化Prompt.md
```

### 注意事项

- ✅ **自动引用**：推荐后立即@引用，无需用户手动操作
- ✅ **路径准确**：使用上述映射表中的准确文件路径
- ✅ **顺序执行**：多个Prompt按推荐顺序依次执行
- ⚠️ **文件名注意**：`技术内容思路构建Promot.md` 文件名中为"Promot"（非"Prompt"）
