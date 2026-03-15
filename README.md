# qiao-skills

> 面向 Agent 的技能仓库，提供可复用的全局规范与项目定制 skill，支持按 `global/` 和 `project/` 分层安装。

## 快速开始

### 一键安装 `global/` 全量（推荐）

```bash
npx -y skills add https://github.com/qiao-925/qiao-skills/tree/main/global --all --full-depth --global --yes
```

- 该命令只扫描 `global/`，不会把 `project/` 里的项目定制技能装进全局作用域。
- `--full-depth` 会递归发现分组目录下的 skills，适合当前仓库这种“分组 + 子目录”结构。

### 按项目安装定制 skills

```bash
npx -y skills add https://github.com/qiao-925/qiao-skills/tree/main/project/project-guide-assemble --yes
npx -y skills add https://github.com/qiao-925/qiao-skills/tree/main/project/project-guide-cs-rag --yes
```

### 更新已安装 skills

```bash
# 检查全局（global）已安装 skills 是否有更新
npx -y skills check --global

# 一键更新全局（global）已安装 skills
npx -y skills update --all --global --yes

# 检查当前项目已安装的 skills 是否有更新
npx -y skills check

# 一键更新当前项目已安装的 skills
npx -y skills update --all --yes
```

## 目录结构说明

```text
.
├── README.md
├── gitignore-global.example
├── global
│   ├── agent-collaboration
│   │   ├── ai-collaboration-principles
│   │   ├── critical-thinking-guidance
│   │   ├── doc-driven-development
│   │   ├── review-separation-guard
│   │   └── roi-value-density
│   ├── agent-workflow
│   │   ├── checkpoint-persistence
│   │   └── workflow
│   ├── agent-skill-rules
│   ├── architecture-governance
│   ├── code-complexity-control
│   │   ├── core-first-simplicity
│   │   ├── file-header-comments
│   │   ├── file-size-limit
│   │   └── project-principles
│   ├── language-engineering-python
│   │   ├── python-coding-standards
│   │   └── python-uv-acceleration
│   ├── project-documentation
│   │   └── technical-readme-structure
│   └── single-responsibility
└── project
    ├── project-guide-assemble
    │   ├── prompt-recommendation
    │   └── whetstone
    └── project-guide-cs-rag
        └── cs-rag-architecture-guideline
```

上面的目录树主要展示“分组和 skill 名称”，各目录职责如下：

- `README.md`：仓库入口文档，负责说明安装方式、目录组织和使用约定。
- `gitignore-global.example`：全局 Git 忽略模板，避免 `.agents/` 等安装产物进入版本控制。
- `global/`：通用 skill 根目录，适合跨项目复用和全局安装。
- `global/agent-collaboration/`：Agent 协作类规则，覆盖协作原则、思考引导、文档驱动开发、审查隔离和 ROI 判断。
- `global/agent-workflow/`：任务阶段路由与关键节点持久化规则，覆盖 `workflow` 与 `checkpoint-persistence` 两个 skill。
- `global/agent-skill-rules/`：skill 本身的设计与治理规范，约束结构、frontmatter、渐进式披露和质量门禁。
- `global/architecture-governance/`：架构治理类规则，聚焦分层约束、接口契约、依赖方向和影响面分析。
- `global/code-complexity-control/`：复杂度控制类规则，约束简化原则、文件头注释、文件大小和项目聚焦。
- `global/language-engineering-python/`：Python 工程实践规则，覆盖编码标准与 `uv` 工具链加速。
- `global/project-documentation/`：项目文档规则分组，目前包含技术项目 README 结构规范。
- `global/single-responsibility/`：单一职责专项规则，强调文件、函数、模块职责边界清晰。
- `project/`：项目定制 skill 根目录，不建议全局批量安装，适合进入具体项目后按需使用。
- `project/project-guide-assemble/`：Assemble 项目相关技能，偏内容组织、提示词编排与结构化整理。
- `project/project-guide-cs-rag/`：CS-RAG 项目专用技能，聚焦该项目的架构认知与设计约束。
- 每个 skill 目录都以 `SKILL.md` 为入口，必要时再挂接 `references/`、`scripts/`、`assets/` 提供补充说明或辅助资源。

### 全局 gitignore（建议）

**PowerShell（Windows）**

```powershell
Copy-Item -Force .\gitignore-global.example $env:USERPROFILE\.gitignore_global
git config --global core.excludesfile "$env:USERPROFILE\.gitignore_global"
```

**Bash（macOS/Linux）**

```bash
cp -f ./gitignore-global.example ~/.gitignore_global
git config --global core.excludesfile ~/.gitignore_global
```
