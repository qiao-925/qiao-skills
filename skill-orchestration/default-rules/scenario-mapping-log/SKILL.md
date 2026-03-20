---
name: scenario-mapping-log
description: 场景映射日志默认规则，用一张简洁的场景映射表提升 skill 调用的可解释性。它不强控路由，只维护场景预期，并在运行中比较 expected、actual、missing 与 unexpected，帮助定位是场景判断、skill 描述还是映射表需要优化。适用于 skill 体系设计、调试、重构、命中偏差排查，以及用户显式要求做场景映射校验的场景。关键词：scenario mapping、mapping log、场景映射、场景校验、命中校验、skill coverage、explainability、expected、actual、missing、unexpected。
metadata:
  type: declarative
  category: scenario-governance
  role: default-rule
---

# 场景映射日志

> 场景分类的价值，不是控制 skill 调用，而是增强 skill 命中的可解释性，并为后续优化提供依据。

## 核心原则

### 1. 这是解释层，不是强路由

- 本规则不伪装成真实底层调用链。
- 本规则不负责强制 `router -> scenario -> unit`。
- 本规则只回答：当前任务理论上应命中什么，运行中实际上命中了什么，偏差更像该优化哪里。

### 2. 实现本身必须可理解

- 场景表要一眼能读懂，不能为了“看起来严谨”把解释层做成小框架。
- 场景按“当前主问题”划分，不按世界的完整分类学划分。
- 映射层级默认只保留 `Core / Conditional` 两层。
- 启用条件也要简单可理解：默认关闭，按需触发，而不是每次任务都自动跑一遍。

### 3. 默认只做预期与实际比对

- `expected`：来自 `references/scenario-map.md`
- `actual`：按 `references/actual-hit-sources.md` 的来源顺序收集运行中的真实命中记录；若没有可靠记录，则写 `unavailable`
- 默认比较结果只保留：
  - `matched`
  - `missing`
  - `unexpected`

### 4. 偏差的价值在于指导优化

- `missing` 不自动等于失败，它首先是一个排查信号。
- 优先排查四类原因：
  - 主场景判断错了
  - skill 描述或触发语义写偏了
  - 映射表期待不合理
  - 当前存在合理直连，不必强行回到预期路径

## AI Agent 行为要求

### 默认步骤

1. 判断当前任务是否存在稳定的 `primary scenario`。
2. 从 `references/scenario-map.md` 读取该场景的 `Core / Conditional`。
3. 按 `references/actual-hit-sources.md` 收集 `actual` 命中记录；若没有底层 telemetry，则改用 checkpoint、任务记录或人工复盘的最小日志。
4. 对照 `expected` 与 `actual`，给出 `matched / missing / unexpected`。
5. 若存在偏差，直接说明下一步应优化哪里。
6. 若没有稳定主场景，或没有可靠 `actual`，不要强行套表。

### 触发条件

默认不启用完整映射日志。以下两类情况再启用：

- 任务本身属于 skill 系统设计、迁移、重构、调试或命中偏差排查
- 用户显式使用触发词要求做映射校验

推荐显式触发词：

- `场景映射`
- `场景校验`
- `命中校验`
- `映射日志`
- `mapping log`
- `scenario mapping`

如果用户只是普通执行任务，且没有出现明显偏差：

- 不外显映射日志
- 不为了“完整性”额外生成一份分析

### `actual` 命中记录的默认来源顺序

为避免 `scenario-mapping-log` 只停留在“映射表 + 空格式”，当前仓库约定按以下顺序收集 `actual`：

1. 平台或运行时原生命中日志
2. 任务执行中的结构化记录，例如 checkpoint、任务日志、阶段复盘
3. 人工复盘得到的命中清单

最小闭环要求：

- 只在 skill 系统设计、迁移、调试、偏差排查、阶段复盘这些高价值场景下要求补记录
- 普通任务没有偏差时，不要求每轮都额外写一份命中日志
- 一旦进入映射校验场景，至少应留下 1 条可回看的 `actual` 记录，而不是只保留 `expected`

最小记录模板见 `references/actual-hit-sources.md`。

### 默认输出格式

```text
Primary Scenario:
- documentation/readme

Expected:
- Core: technical-readme-structure
- Conditional: value-dense-delivery, readability-first-writing

Actual:
- technical-readme-structure
- readability-first-writing

Matched:
- technical-readme-structure
- readability-first-writing

Missing:
- value-dense-delivery

Unexpected:
- none
```

如果当前没有稳定主场景，或没有可靠运行记录：

```text
Primary Scenario:
- none

Expected:
- none

Actual:
- unavailable

Notes:
- 当前没有稳定主场景或可靠命中记录，暂不做映射比对
```

### 何时应外显映射日志

- skill 系统设计、迁移、重构、调试
- 用户明确询问为什么没命中预期 skill
- 用户手上已经有一份实际命中记录，需要与场景映射比对
- 当前怀疑某个 skill 的描述、边界或映射关系写偏了
- 用户显式使用了 `场景映射 / 场景校验 / 命中校验 / 映射日志 / mapping log / scenario mapping` 等触发词

普通任务执行中：

- 不要求每次都外显映射日志
- 但如果要做映射校验，默认也应沿用同一套简单格式

### 映射维护原则

- 映射表优先引用当前仓库中真实存在、仍在维护的 skill。
- 场景拆分的标准不是“分类是否漂亮”，而是“能否支持后续优化”。
- 如果两个场景的预期 skill 和后续优化动作几乎一样，就不值得硬拆。
- 如果一个场景长期只制造解释负担，而不能指导优化，就应该合并或删除。

## 判断标准

- 场景名是否让人一眼知道“当前主问题是什么”。
- 映射表是否保持低认知负担，而不是不断加中间概念。
- 比对格式是否仍然围绕 `expected / actual / missing / unexpected`。
- 做映射校验时，是否至少能拿到 1 条可回看的 `actual` 记录，而不是完全靠回忆重建。
- 出现偏差时，是否能落到具体优化动作，而不是停留在抽象解释。

## 反模式

- 把场景映射表写成强控制调度器。
- 把解释层做成过重的协议系统。
- 为了追求完备而把场景越拆越碎。
- 没有稳定主场景时，仍然强行比对。
- 发现偏差后只说“没命中”，却不指出应该优化哪里。

## 参考资料

- `references/scenario-map.md` - 当前仓库场景映射表：只维护“场景 -> 预期 skill”的映射关系
- `references/log-comparison-format.md` - 最小命中比对格式：`expected / actual / matched / missing / unexpected`
- `references/actual-hit-sources.md` - `actual` 命中记录的来源顺序、最小记录模板与适用边界
