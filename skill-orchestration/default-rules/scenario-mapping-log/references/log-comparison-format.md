# 命中比对格式

> 这个文档只回答一件事：如何把场景映射里的 `expected`，和运行中的 `actual` 做最小比对。

## 1. 最小字段

### `expected`

- 来源：`references/scenario-map.md`
- 含义：当前主场景理论上应命中的 skill
- 展示方式：按 `Core / Conditional` 展开

### `actual`

- 来源：运行时真实命中记录
- 含义：这次任务里实际上命中的 skill
- 注意：如果没有可靠来源，写 `unavailable`

### `matched`

- 定义：`expected` 与 `actual` 的重合部分
- 含义：这次命中与预期一致的部分

### `missing`

- 定义：理论上应命中，但 `actual` 中没有出现的 skill
- 含义：优先排查的偏差信号

### `unexpected`

- 定义：`actual` 中出现，但不在当前场景预期内的 skill
- 含义：说明主场景判断、skill 触发边界或映射设计可能需要回看

## 2. 推荐格式

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

如果没有可靠运行记录：

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

## 3. 如何解读偏差

### `missing` 很多

优先回看：

- 主场景是否判断错了
- skill 的触发语义是否写偏了
- 映射表期待是否过高
- 当前是否存在合理直连

### `unexpected` 很多

优先回看：

- 当前主场景是否选偏了
- 某些 skill 是否触发范围过宽
- 某些 skill 是否应该被吸纳进当前场景的 `Conditional`

## 4. 使用边界

- 这是解释与优化格式，不是底层 telemetry 协议。
- 它只负责比对命中预期，不负责证明结果质量。
- 如果后续需要评估“结果虽然没命中但实际上已经做到了”，那属于第二层诊断，不放进默认格式。
