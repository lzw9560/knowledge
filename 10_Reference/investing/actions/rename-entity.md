---
type: action
action_id: RENAME-ACT-001
action_type: 链接维护
trigger: 实体改名时，重写所有反向链接
target: 全类型
audit: true
created: 2026-09-07
---

# 动作：实体改名重写反向链接

## 动作定义

- **类型**：链接维护
- **触发条件**：实体文件移动/重命名（需人工触发，agent 不可直接调用）
- **目标实体**：全类型（stocks/industries/concepts/specs 等）
- **审计**：true（改名日志）

## 执行步骤

1. 校验调用方：if agent 直接调用 → 拒绝（ora-3 §6.5）；if 人工调用 → 继续
2. 执行 `move_note(old_path, new_path)`：
   - 移动/重命名文件
   - 扫描全库 `[[链接]]`，把指向 old_path 的链接重写为 new_path
   - 处理别名（`[[old|alias]]` → `[[new|alias]]`）
3. 记录改名日志（who/when/old/new）到 `reviews/`

## 审计点

- 执行前状态：旧路径文件 + 全库反向链接清单
- 执行后状态：新路径文件 + 反向链接已重写
- 异常处置：重写失败（部分文件只读）→ 告警 + 列出未重写的链接

## 安全约束

- `move_note` 是危险操作，只对人工开放（ora-3 §6.5）
- agent 若需改名应：建 inbox 新实体 → 提交改名工单 → 人工审核后执行

## 关联

- 触发自：[[logic/实体改名]]（RENAME-001）
- 作用于：全类型
- 执行记录：[[reviews/]]
