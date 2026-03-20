# `actual` 命中记录来源顺序

> 这个文档只回答一件事：在没有底层 telemetry 协议的前提下，`scenario-mapping-log` 的 `actual` 从哪里来，以及怎样形成最小可复盘闭环。

## 1. 来源顺序

### P0：平台或运行时原生命中日志

- 例如：平台显式记录了本轮实际调用的 skill
- 这是最优来源，优先级最高
- 若存在此类日志，默认直接使用

### P1：任务执行中的结构化记录

- 例如：checkpoint、任务日志、阶段复盘、handoff 说明
- 条件：记录中显式写出了本轮实际命中的 skill
- 这是当前仓库默认推荐的无 telemetry 闭环方式

### P2：人工复盘

- 例如：在做命中偏差排查时，基于任务记录或对话复盘补一条命中清单
- 仅在 P0 / P1 缺失时使用
- 使用时应显式标注来源为 `manual-review`

如果三者都没有，`actual` 写 `unavailable`，不要伪造记录。

## 2. 何时必须补一条 `actual` 记录

以下场景至少应留下 1 条可回看的 `actual` 记录：

- skill 系统设计
- skill 迁移或重构
- 命中偏差排查
- 场景映射校验
- 阶段复盘

以下场景不强制补记录：

- 普通执行任务且没有明显偏差
- 极短任务、低价值任务
- 没有任何映射校验诉求的日常交互

## 3. 最小字段

最少保留以下字段：

- `Task`：当前任务或问题的简短标识
- `Time`：记录时间
- `Primary Scenario`：若已判断出主场景则写；否则可写 `none`
- `Actual`：本轮实际命中的 skill 列表
- `Actual Source`：`runtime-log / checkpoint / task-log / manual-review`
- `Reliability`：`high / medium / low`

可选字段：

- `Notes`：补充为什么命中这些 skill，或为什么记录可信度较低

## 4. 最小模板

```text
Task:
- review current skill repo readiness

Time:
- 2026-03-20T11:30:00+08:00

Primary Scenario:
- skill-system/design

Actual:
- agent-skill-rules
- scenario-mapping-log
- technical-readme-structure

Actual Source:
- task-log

Reliability:
- medium

Notes:
- 基于本轮任务记录整理，无平台原生命中日志
```

## 5. 默认落点

优先把这条最小记录写进以下位置之一：

- 阶段性 checkpoint
- 任务调试笔记
- 研究/复盘文档
- issue / comment / handoff 记录

不要为了记录 `actual` 单独发明复杂协议、数据库或重型框架。

## 6. 使用边界

- 这不是底层 telemetry 协议，只是解释层的最小闭环方案。
- 它解决的是“事后还能不能回看这轮到底命中了什么”，不是“百分之百精准自动埋点”。
- 当前仓库优先追求低成本可执行，而不是形式上的完美完备。
