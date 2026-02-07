# 分层与依赖方向基线

## 1. 分层目标

保持职责边界清晰，避免技术实现与业务规则相互污染。

---

## 2. 通用分层模型

```
接口/交互层（Presentation）
        ↓
应用/业务层（Application/Business）
        ↓
基础设施层（Infrastructure）
```

- 上层编排流程与规则，下层提供能力实现
- 默认只允许相邻层依赖

---

## 3. 依赖方向规则

### 允许

- Presentation → Application
- Application → Infrastructure

### 禁止

- Infrastructure → Application（反向依赖）
- Presentation → Infrastructure（跨层直连）
- 任意双向依赖（循环耦合）

---

## 4. 快速检查清单

- [ ] 每个模块能明确归属某一层
- [ ] 新增 import 不破坏依赖方向
- [ ] 无循环依赖

