# AI Agent Rules 规范调研

> 调研目标：梳理主流 AI coding assistant 的 rule 规范、写作最佳实践与共性约束，为 qiao-skills → rules 迁移提供依据。

## 阅读路线

1. **结构视角**：rule 在各平台的格式、激活机制、存储位置
2. **写作原则**：跨平台共识的 rule 写作最佳实践
3. **关键约束**：LLM 注意力与指令跟随能力的硬限制
4. **迁移启示**：对 qiao-skills 迁移方案的影响

---

## 一、各平台 Rule 规范对比

### 1.1 格式与激活机制

| 平台 | 文件位置 | 格式 | 激活方式 | 长度限制 |
|------|----------|------|----------|----------|
| **Windsurf** | `.windsurf/rules/*.md` | Markdown + YAML frontmatter | `always_on` / `model_decision` / `glob` / `manual` | 12,000 字符/文件 |
| **Cursor** | `.cursor/rules/*.mdc` | MDC (Markdown + metadata) | Always On / Auto Attached / Model Decision / Manual | 无官方上限，建议精简 |
| **Claude Code** | `CLAUDE.md` + `.claude/rules/*.md` | 纯 Markdown（rules 支持 `paths` frontmatter） | 自动加载；rules 可按路径作用域 | 建议 < 300 行 |
| **GitHub Copilot** | `.github/copilot-instructions.md` + `.github/instructions/*.instructions.md` | Markdown + `applyTo` frontmatter | 全局 / glob 匹配 | 无官方上限 |
| **AGENTS.md** | 仓库任意目录 | 纯 Markdown，无 frontmatter | 根目录 = always on；子目录 = 自动作用域 | Codex CLI 默认 64KB |

### 1.2 Frontmatter 对比

**Windsurf**：
```yaml
---
trigger: model_decision          # always_on / model_decision / glob / manual
description: "触发条件描述"       # model_decision 时必填
globs: "**/*.py"                  # glob 时必填
---
```

**Cursor**（MDC 格式）：
```
---
description: "规则描述"
globs: "**/*.tsx"
alwaysApply: false
---
```

**Claude Code**（`.claude/rules/` 内）：
```yaml
---
paths:
  - "src/api/**/*.ts"
---
```

**GitHub Copilot**：
```yaml
---
applyTo: "**/*.tsx"
---
```

### 1.3 共性发现

所有平台都收敛到同一个核心思路：

> **仓库中的 Markdown 文件 + 元数据控制激活范围**

差异仅在命名和作用域粒度上。

---

## 二、Rule 写作最佳实践（跨平台共识）

### 2.1 核心约束：LLM 的指令跟随能力有上限

来源：HumanLayer 引用的研究（arxiv.org/pdf/2507.11538）

- 前沿 thinking 模型可稳定跟随 **~150-200 条指令**
- 小模型衰减更快（指数级），前沿模型衰减更慢（线性）
- **Claude Code 系统提示已占用 ~50 条指令**，留给用户的预算有限
- 随着指令数增加，**所有指令的跟随质量均匀下降**——不是只忽略后面的，而是全部变差
- LLM 对上下文窗口**首尾**的指令关注度更高（首因/近因效应）

**关键结论：rule 文件应尽可能精简，只保留当前任务普遍适用的指令。**

### 2.2 黄金法则

#### 精简优先（Less is more）

- **50 行精准 > 1000 行发散**
- HumanLayer 的根 `CLAUDE.md` 不到 60 行
- 一个专注的 50 行文件优于一个大而全的 500 行文件
- 每一行都应该"值得占用上下文窗口预算"

#### 渐进式披露（Progressive Disclosure）

- 核心指令放在主 rule 文件
- 详细参考、模板、示例放在独立文件，按需加载
- 用指针（"参见 X 文件"）代替复制内容
- 这正是 Windsurf `model_decision` 和 Cursor `Auto Attached` 的设计意图

#### 具体可验证（Specificity）

好的 rule：
- "使用 2 空格缩进"
- "运行 `npm test` 再提交"
- "API handler 放在 `src/api/handlers/`"

差的 rule：
- "写好代码"
- "测试你的改动"
- "保持文件有序"

#### 普遍适用（Universal Applicability）

- always-on 的 rule 内容应在**绝大多数会话**中都有用
- 特定场景的指令不应放在全局 rule 中
- 如果一条 rule 只在 10% 的会话中有用，它放在 always-on 里会在 90% 的时间浪费预算并干扰模型

### 2.3 应该放进 Rule 的内容

| 类别 | 示例 |
|------|------|
| 构建与测试命令 | `npm run build`、`pytest -x` |
| 技术栈与版本 | Next.js 15、Python 3.11、PostgreSQL 16 |
| 项目结构 | `src/` 各目录的职责说明 |
| 关键约定 | 命名导出、错误响应格式、迁移文件位置 |
| 不可猜到的约束 | 特殊的部署流程、安全要求、分层规则 |

### 2.4 不应放进 Rule 的内容

| 类别 | 原因 | 替代方案 |
|------|------|----------|
| 代码风格规则 | ESLint/Prettier/Ruff 做得更快更确定 | 用 linter + formatter |
| 显而易见的事 | "写好代码" 浪费预算 | 删除 |
| 完整 API 文档 | 太长，应按需查阅 | `agent_docs/` 目录 + 指针 |
| 特定任务指令 | 不普遍适用 | 放在 prompt 或 model_decision rule |
| 大段代码片段 | 容易过时，浪费上下文 | 用 file:line 引用 |

### 2.5 常见错误

1. **写太长**：超过 500 行的大部分内容被忽略
2. **跨工具复制**：维护一个 AGENTS.md 作为唯一真相源
3. **用 /init 自动生成**：生成的内容通常泛泛且臃肿
4. **包含 linter 规则**：让确定性工具做确定性工具的事
5. **忘记更新**：错误的指令比没有指令更糟

---

## 三、Rule vs Skill vs Workflow 定位

| 维度 | Rule | Skill | Workflow |
|------|------|-------|----------|
| **本质** | 行为准则（怎么做） | 多步骤过程 + 支撑文件 | 可重复任务的 prompt 模板 |
| **结构** | 单个 .md + frontmatter | 文件夹（SKILL.md + resources） | 单个 .md |
| **激活** | always_on / glob / model_decision / manual | 模型决定 或 @mention | 仅手动 /slash-command |
| **系统提示占用** | 取决于激活模式 | 仅名称+描述，调用时加载全文 | 不占用 |
| **适合** | 编码规范、项目约束、短行为约束 | 需要模板/脚本的复杂任务 | 部署、发布、review 检查单 |

**判断法**：
- 如果是短的行为约束 → **Rule**
- 如果需要支撑文件且应自动匹配 → **Skill**
- 如果总是手动触发 → **Workflow**

---

## 四、对 qiao-skills 迁移的关键启示

### 4.1 当前方案的问题

已创建的 `always_on` rule 文件（如 `human-steered-execution.md`）合并了 SKILL.md + 全部 references，导致：

- 文件长度 **150-360+ 行**，远超行业推荐的 < 100 行
- always_on 内容全量进入系统提示，**每条消息都消耗这些 token**
- 5 个 always_on rule 加起来可能 **1000+ 行**，严重挤压上下文预算
- LLM 指令跟随质量会随指令数增加而均匀下降

### 4.2 建议调整方向

#### always_on：精简到核心原则

- 每个 always_on rule 控制在 **30-80 行**
- 只保留核心原则和判断标准
- 删除详细展开、示例、模板、反模式清单
- 详细内容降级为 model_decision 或独立参考文件

#### model_decision：利用渐进式披露

- description 写清触发条件（这是模型判断是否加载全文的唯一依据）
- 全文可以较长，但仍需控制在 12,000 字符以内
- 合并 references 是合理的，因为全文只在需要时加载

#### glob：文件类型精准匹配

- Python 规则只在 `*.py` 时加载，不浪费其他场景的预算

### 4.3 内容分层建议

```
always_on rule（30-80 行）
  ├── 核心原则（3-5 条）
  ├── 最低要求表（一个表格）
  └── 判断标准（3-5 条 checklist）

model_decision rule（100-300 行）
  ├── description: 清晰的触发条件描述
  ├── 核心原则 + 展开说明
  ├── AI Agent 行为要求
  ├── 场景化参考（原 references 合并）
  └── 反模式
```

### 4.4 质量框架（对应三个归档 skill 的思想迁移）

原 `agent-skill-rules` / `skill-audit` / `scenario-mapping-log` 的核心思想：

- **rule 约束**：rule 本身需要规范（frontmatter、长度、激活模式选择）
- **rule 审计**：修改后应检查质量（长度、具体性、普遍适用性）
- **运行时验证**：rule 实际被遵循的程度

这些可以沉淀为一个 **rule 质量检查清单**，而不是独立的 rule 文件。

---

## 五、调研来源

| 来源 | 类型 | 关键贡献 |
|------|------|----------|
| [Windsurf 官方文档](https://docs.windsurf.com/windsurf/cascade/memories) | 一手 | 激活模式、frontmatter 规范、字符限制 |
| [Cursor 官方文档](https://docs.cursor.com/context/rules) | 一手 | MDC 格式、作用域机制 |
| [Claude Code 官方文档](https://code.claude.com/docs/en/memory) | 一手 | CLAUDE.md 加载机制、rules/ 路径作用域、@import |
| [HumanLayer: Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) | 近一手 | 指令跟随能力研究、渐进式披露、具体建议 |
| [DeployHQ: Configure Every AI Coding Assistant](https://www.deployhq.com/blog/ai-coding-config-files-guide) | 综合 | 全平台格式对比、最佳实践、常见错误 |
| [AGENTS.md 官方站](https://agents.md/) | 一手 | 开放标准、Linux Foundation 治理 |
| 论文 arxiv.org/pdf/2507.11538 | 一手 | LLM 指令跟随衰减曲线 |
