# Agent Skills 格式规范

> 来源：[agentskills.io/specification](https://agentskills.io/specification)  
> 本文档为官方 Specification 的引用，供编写 skill 时查阅。

---

## Directory structure

Skill 是至少包含一个 `SKILL.md` 的目录：

```
skill-name/
└── SKILL.md          # Required
```

可选的 [additional directories](#optional-directories) 包括：`scripts/`、`references/`、`assets/`。

---

## SKILL.md format

`SKILL.md` 必须包含 YAML frontmatter，后接 Markdown 正文。

### Frontmatter（必填）

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

可选字段示例：

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

| Field | Required | Constraints |
| ----- | -------- | ----------- |
| `name` | Yes | Max 64 字符。仅小写字母、数字、连字符。不能以连字符开头或结尾。 |
| `description` | Yes | Max 1024 字符。非空。描述技能做什么、何时使用。 |
| `license` | No | 许可证名称或对 bundled 许可证文件的引用。 |
| `compatibility` | No | Max 500 字符。环境要求（目标产品、系统依赖、网络等）。 |
| `metadata` | No | 任意 key-value，供客户端扩展。 |
| `allowed-tools` | No | 空格分隔的预批准工具列表。（实验性） |

#### name

- 1–64 字符
- 仅 `a-z` 与 `-`
- 不能以 `-` 开头或结尾
- 不能含连续连字符 `--`
- 必须与父目录名一致

合法示例：`pdf-processing`、`data-analysis`、`code-review`  
非法示例：`PDF-Processing`、`-pdf`、`pdf--processing`

#### description

- 1–1024 字符
- 应同时说明「做什么」和「何时用」
- 应含便于代理匹配的关键词

推荐：*Extracts text and tables from PDF files... Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.*  
不推荐：*Helps with PDFs.*

#### license（可选）

许可证名称或简短说明，如：`Proprietary. LICENSE.txt has complete terms`。

#### compatibility（可选）

- 若填写，1–500 字符
- 仅在有明确环境要求时填写
- 可写目标产品、系统包、网络等

示例：*Designed for Claude Code (or similar products)* / *Requires git, docker, jq, and access to the internet*。  
多数 skill 不需要此字段。

#### metadata（可选）

字符串 key → 字符串 value。建议 key 命名具一定唯一性，避免冲突。

#### allowed-tools（可选）

空格分隔的、允许该 skill 调用的工具列表。实验性，各实现支持不一。  
示例：`allowed-tools: Bash(git:*) Bash(jq:*) Read`。

---

### Body content

Frontmatter 之后的 Markdown 为技能说明，格式不限，以便代理执行为准。

建议包含：

- 分步说明（Instructions）
- 输入/输出示例
- 常见边界情况（Edge cases）

代理在激活 skill 时会加载整个文件。正文过长时，建议拆到引用文件中。

---

## Optional directories

### scripts/

可执行代码。脚本应：

- 自包含或明确写出依赖
- 提供清晰的错误信息
- 妥善处理边界情况

支持语言取决于具体 agent，常见为 Python、Bash、JavaScript。

### references/

按需加载的补充文档，例如：

- `REFERENCE.md` — 详细技术说明
- `FORMS.md` — 表单/结构化数据模板
- 领域文件（如 `finance.md`、`legal.md`）

单文件保持聚焦，便于按需加载、节省 context。

### assets/

静态资源：模板、图片、数据文件（查找表、schema 等）。

---

## Progressive disclosure

建议分层使用 context：

1. **Metadata**（约 100 tokens）：所有 skill 启动时加载 `name`、`description`
2. **Instructions**（建议 < 5000 tokens）：激活时加载完整 `SKILL.md` 正文
3. **Resources**（按需）：`scripts/`、`references/`、`assets/` 中的文件仅在需要时加载

**保持主 `SKILL.md` 在 500 行以内**，详细内容放到单独文件。

---

## File references

从 skill 根目录出发，用相对路径引用其他文件：

```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

从 `SKILL.md` 出发的引用保持**一层深度**，避免深层嵌套引用链。

---

## Validation

使用 [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) 校验：

```bash
skills-ref validate ./my-skill
```

会检查 `SKILL.md` frontmatter 及命名是否符合规范。
