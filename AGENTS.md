# qiao-skills Agent 规则

## Skill 创建与更新规则

创建新 skill 或更新现有 skill 时，必须先调用 `@agent-skill-rules`，按其流程执行：

- Pre-Step：判断需求是否应该 skill 化（能脚本化的不做 skill）
- Step 1–3：目录结构、frontmatter、正文结构均须符合规范
- 类型必须明确（procedural / declarative），正文结构与类型匹配

## Skill 审查规则

对仓库中任何 `SKILL.md` 文件进行修改后，必须自动执行 `@skill-audit` 对被修改的 skill 进行静态审查：

- 读取被修改的 `SKILL.md`
- 检查 frontmatter（name、description、type）是否符合规范
- 检查 description 是否包含触发条件和关键词
- 检查正文结构是否与 skill 类型匹配（procedural 用 Instructions，declarative 用核心原则）
- 检查是否存在冗余章节或内容重复
- 输出审查报告：通过 / 需要调整（附具体问题）

若只修改文档（如 `README.md`、`references/`）可跳过。

若审查发现问题，需输出具体问题清单并等待修复，不要直接推送。

## 审查通过后自动发布

`@skill-audit` 审查结论为"✅ 通过"后，自动执行以下步骤：

1. `git add -A`
2. `git commit -m "chore: update skill <skill-name>"`
3. `git push`
4. `npx -y skills update --all --global --yes`

若任意步骤失败，输出错误原因并停止，不继续后续步骤。
