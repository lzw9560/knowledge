---
type: action
action_id: RENAME-ACT-001
action_type: 链接维护
trigger: 实体改名时，重写所有反向链接
target: 全类型
audit: true
created: 2026-09-07
confidence: high
source: logic_rules
---

> [!info] ⚡ 动作
> **动作**：`RENAME-ACT-001`  **类型**：链接维护
> **触发**：`实体改名时，重写所有反向链接`  **目标**：`全类型`
>
> **触发自**：[[logic/]]

## 📋 动作定义

- 类型：`链接维护`
- 触发：`实体改名时，重写所有反向链接`
- 目标：`全类型`


## 🔧 执行步骤

1. 校验调用方：if agent 直接调用 → 拒绝（ora-3 §6.5）；if 人工调用 → 继续
2. 执行 `move_note(old_path, new_path)`：
   - 移动/重命名文件
   - 扫描全库 `[[链接]]`，把指向 old_path 的链接重写为 new_path
   - 处理别名（`[[old|alias]]` → `[[new|alias]]`）
3. 记录改名日志（who/when/old/new）到 `reviews/`


## 🔍 审计点

- 执行前状态：旧路径文件 + 全库反向链接清单
- 执行后状态：新路径文件 + 反向链接已重写
- 异常处置：重写失败（部分文件只读）→ 告警 + 列出未重写的链接


## 🔗 关联

- **触发自**：[[logic/]]
- **作用于**：[[stocks/]]
- **执行记录**：[[reviews/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
