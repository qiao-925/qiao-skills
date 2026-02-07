# Skill 类型分类学：动作型 vs 约束型

> 日期：2026-02-06
> 背景：在为 qiao-skills 创建 AI 协作相关 skill 时，发现 Agent Skills 官方规范对不同类型 skill 的适配性存在结构性缺口。

---

## 起因：用户提问

在完成 3 个 AI 协作相关 skill（`ai-collaboration-principles`、`doc-driven-development`、`critical-thinking-guidance`）的创建后，用户提出了以下观察：

- `agent-skill-rules`（创建 skill 的 skill）中有分步说明的 flow：按什么步骤去做 1-2-3
- 这种步骤式结构对功能性规则、有执行动作的 skill 是适用的
- 但对于一些**静态规则**，比如 AI 协作原则（理解需求、批判性思维、保持专注、质量优先），很难按步骤展开
- 这些内容更像是一种持续性的约束，而不是一个可执行的流程
- **Agent Skills 规范本身是否存在不足？** 对于不同类型的 skill，是否需要不同的组织方式？

---

## 分析：Agent Skills 规范对"静态规则类 skill"的适配性

### 规范的隐含假设

官方 specification 在 Body content 部分推荐的三要素是：

> - **Instructions**（分步说明）
> - **Examples**（输入/输出示例）
> - **Edge cases**（边界情况）

这三个要素有一个共同的隐含假设：**skill 是一个有明确触发、有执行步骤、有可观测输出的"动作"**。这对 `w02-task-planning`（规划任务）、`w03-testing-and-diagnostics`（测试诊断）这类 skill 非常合适——它们确实有清晰的 input → process → output 流。

但观察是对的：**并非所有 skill 都是"动作型"的**。

### 两种本质不同的 skill 类型

| 维度 | 动作型 skill (Procedural) | 约束型 skill (Declarative) |
|------|--------------------------|---------------------------|
| 本质 | "做什么、怎么做" | "是什么、不能做什么" |
| 触发方式 | 明确事件触发（用户指令、条件满足） | 始终生效，作为背景约束 |
| 执行模式 | 线性步骤：Step 1 → 2 → 3 | 并行检查：每个决策点都要对照 |
| 输入/输出 | 有明确的输入和可观测输出 | 没有独立输出，体现在其他动作的质量上 |
| 示例 | `w02-task-planning`, `doc-driven-development` | `ai-collaboration-principles`, `single-responsibility` |

`doc-driven-development` 其实处于中间地带——它有明确的触发条件（遇到 API 报错时）和执行步骤（停止猜测 → 查文档 → 基于文档实现），所以它用 Instructions 模式是合理的。

但 `ai-collaboration-principles` 就不同了。"批判性思维优先"不是一个你在某个时刻"执行"的步骤，而是一个**贯穿所有交互的持续性约束**。把它硬塞进 Step 1-2-3 的框架，要么变得牵强，要么丢失了它作为"始终生效的原则"的本质。

### 规范的不足之处

1. **缺少 skill 类型分类**。规范把所有 skill 当作同质的，没有区分 procedural vs. declarative。这导致写约束型 skill 时，要么硬套 Instructions 格式（不自然），要么自由发挥（缺乏指导）。

2. **"何时用"的描述对约束型 skill 不够精确**。description 要求写"何时用"，但约束型 skill 的答案是"始终"——这在匹配触发上没有区分度。

3. **缺少"生效方式"的元数据**。规范没有提供字段来区分"按需激活"和"始终加载"。实际上，`ai-collaboration-principles` 这类 skill 理想状态是作为 system prompt 的一部分始终存在，而不是被某个关键词触发后才加载。

4. **渐进式披露对约束型 skill 的适用性存疑**。规范建议"激活时加载 SKILL.md，按需加载 references"。但约束型 skill 的核心价值就在于它的规则要被持续记住，如果不加载就等于不存在。

### 但规范也有合理之处

反过来说，规范的"格式不限"（Body content 部分原文是 "格式不限，以便代理执行为准"）其实给了足够的灵活空间。它推荐 Instructions/Examples/Edge cases，但没有**强制**。问题不在于规范禁止了什么，而在于它**没有为约束型 skill 提供对应的最佳实践指导**。

### 实际影响

回看当时创建的 3 个 skill：

- `doc-driven-development` — 动作型，Instructions 模式自然适配，没有问题
- `critical-thinking-guidance` — 有明确触发和步骤（暂停 → 引导 → 等待 → 回答），虽然偏软性，但 Instructions 模式基本适用
- `ai-collaboration-principles` — 纯约束型，在写的时候实际上已经偏离了 Instructions 模式，用的是"行为要求"+"协作姿态表格"这种声明式结构，因为步骤式写法确实不适合它

### 可能的改进方向

如果要增强 `agent-skill-rules` 来覆盖这个缺口，可以考虑：

1. **在 Step 3 中增加约束型 skill 的正文组织建议**，比如：
   - 用"核心原则 → 行为要求 → 判断标准 → 反模式"替代"Instructions → Examples → Edge cases"
   - 明确说明约束型 skill 不需要硬套步骤格式

2. **在 frontmatter 中建议（非强制）标注 skill 类型**，比如通过 metadata 字段：
   ```yaml
   metadata:
     type: declarative  # 或 procedural
   ```

3. **为 description 提供约束型 skill 的写法示例**，把"何时用"替换为"适用范围"

---

## 结论

这是 skill 规范体系在实践中暴露出的一个真实的结构性缺口。Agent Skills 官方规范隐含地假设所有 skill 都是动作型的，但实际使用中存在大量约束型 skill（规则、原则、标准）。需要在 `agent-skill-rules` 中补充对约束型 skill 的组织方式指导，使两种类型的 skill 都有清晰的最佳实践可循。
