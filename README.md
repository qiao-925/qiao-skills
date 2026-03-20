# qiao-skills

> 面向 Agent 的技能仓库，提供可复用的默认规则、skill-units 与少量独立技能，也记录从 Prompt 工程向 Skill 工程演化的迁移实践。

## 快速开始

### 安装 `skill-orchestration/` 全量（推荐）

```bash
npx -y skills add https://github.com/qiao-925/qiao-skills/tree/main/skill-orchestration --all --full-depth --global --yes
```

- 该命令会递归安装 `default-rules/` 与 `skill-units/` 下的全部 skills。
- `--full-depth` 适合当前仓库这种“分组 + 子目录”结构。

### 按需安装根目录独立技能

```bash
npx -y skills add https://github.com/qiao-925/qiao-skills/tree/main/agent-skill-rules --global --yes
npx -y skills add https://github.com/qiao-925/qiao-skills/tree/main/github-checkpoint-persistence --global --yes
```

- `agent-skill-rules/` 是 skill 设计与治理规范。
- `github-checkpoint-persistence/` 是独立的 checkpoint 持久化技能，目前不放在 `skill-orchestration/` 下。

### 更新已安装 skills

```bash
# 检查全局已安装 skills 是否有更新
npx -y skills check --global

# 一键更新全局已安装 skills
npx -y skills update --all --global --yes
```

### 全局 gitignore（建议）


**查看当前配置**

```bash
git config --global --get core.excludesfile
```

输出为空表示当前还没有设置全局 gitignore。

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



## 核心特性

- **默认规则常驻**：`critical-thinking-evaluation`、`source-quality-control`、`value-dense-delivery`、`readability-first-writing`、`human-steered-execution` 等规则负责跨任务质量基线。
- **能力单元按需触发**：把 README、架构、Python、研究、决策等高频主题拆成独立 `skill-unit`，避免一个“大而全”总 skill。
- **治理与迁移分层**：`agent-skill-rules` 负责 skill 设计与治理；`github-checkpoint-persistence` 负责 GitHub 场景下的 checkpoint 持久化。
- **场景映射可解释**：`scenario-mapping-log` 只做解释层，不强控路由；同时维护 `expected` 和 `actual` 的最小闭环。

## 目录结构

```text
qiao-skills
├── root standalone skills
│   ├── agent-skill-rules
│   └── github-checkpoint-persistence
└── skill-orchestration
    ├── default-rules
    │   ├── quality baseline
    │   └── scenario explainability
    └── skill-units
        ├── decision-support
        ├── documentation
        ├── engineering
        ├── language-engineering
        └── research
```

## 从 Prompt 到 Skill：变与不变

近来 AI 工程里的名目，改得很勤。先前叫 Prompt，如今叫 Skill，往后怎样叫，谁也说不定。倘若因此便以为，名字一换，事情也全新了，那大概是容易受一点热闹欺骗的。

其实变的，多半只是容器：写法不同了，安装方法不同了，组织方式不同了，维护起来也比从前讲究些了。至于那些真正值钱的东西，却并不随着名色起落。它们先前可以写在 Prompt 里，今天可以拆进 Skill 里，明天自然也还可以寄住在别的容器里；搬了家，并不等于改了脾气。这次迁移之后，留下的一个更朴素的认识是：Prompt 换成 Skill，变的是工程容器，不是那些真正长期有效的方法。

所以这套仓库想沉淀的，并不只是某个 Prompt，或某个 Skill；较要紧的是那些不大肯过时的判断原则，例如：

- `critical-thinking-evaluation`：重要判断要有结构化评估、反附和、反草率结论。
- `source-quality-control`：外部知识要看来源等级、可溯源性、时效性和结论力度。
- `value-dense-delivery`：输出要追求高信号、高价值密度，而不是冗长堆料。
- `readability-first-writing`：信息不仅要正确，还要让读者更容易理解、跟上和吸收。
- `human-steered-execution`：AI 可以加速执行，但方向权、价值判断权和高代价选择权仍应由人类掌舵。

因此，这个仓库做迁移，并不是把旧 Prompt 改个名字，换件衣裳，就算大功告成；而是想把那些经得起折腾的思想留下来，再替它们换一个在当前阶段更便于安装、组合、观察和维护的壳。大体说来，做的是这几件事：

- 保留那些经久不衰的思想。
- 更换更适合当前阶段的工程容器。
- 将通用能力上收为默认规则或 skill-unit。
- 将强项目语境、低复用频率的模板留在项目侧或作为溯源资产保留。

但这样的整理，也并没有一个现成的完成时。小如自己搭起来的一套 skills，大如外面的世界，都是**一面收拾，一面生长**的。倘若以为今天分了类、立了规则、写了 README，明天便可一劳永逸，那大概又要受一点**定型**两个字的骗。系统刚一安顿，新的任务、新的理解、新的毛病，也就跟着来了。

所以这里所说的“完成”，并不是从此封箱，不许再动；只是到一时一地，先收出一个较清楚、较可用、较能解释自己的样子，好让后面的修改有处着手。能改，并不算它不成；倒是改不得、理不清、越补越乱，才真是麻烦。

所以从这个角度看，`qiao-skills` 与其说只是一个技能仓库，倒不如说也是一份迁移记录：看一套方法，怎样从 Prompt 工程里走出来，住进 Skill 工程里，而把那些真正不该丢的东西，仍旧带在身上。

> 注：本节语气参考鲁迅《随便翻翻》的议论笔调，仅借其说理节奏，不涉原文内容。
