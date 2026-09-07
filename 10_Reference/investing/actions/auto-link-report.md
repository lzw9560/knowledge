---
type: action
action_id: AUTO-LINK-001
action_type: 链接维护
trigger: 报告入库后，扫描正文 6 位代码并建 stocks/{code} 链接
target: reports/, daily/
audit: true
created: 2026-09-07
confidence: high
source: logic_rules
---

> [!info] ⚡ 动作
> **动作**：`AUTO-LINK-001`  **类型**：链接维护
> **触发**：`报告入库后，扫描正文 6 位代码并建 stocks/代码 链接`  **目标**：`reports/, daily/`
>
> **触发自**：[[logic/]]

## 📋 动作定义

- 类型：`链接维护`
- 触发：`报告入库后，扫描正文 6 位代码并建 stocks/代码 链接`
- 目标：`reports/, daily/`


## 🔧 执行步骤

1. 正则扫描报告全文，提取 6 位数字代码（`(00\d{4}|30\d{4}|60\d{4}|68\d{4}|688\d{3})`）
2. 对每个代码：
   - if exists(`stocks/{code}.md`)：在报告"图谱关联"段加 `stocks/{code}`
   - else：在报告"待入图谱"段列出，触发 [[actions/approve-entity]] 的 inbox stub 建档
3. 写回报告（在末尾维护"图谱关联"+"待入图谱"段）


## 🔍 审计点

- 执行前状态：报告原文（无链接段/旧链接段）
- 执行后状态：报告新增"图谱关联"+"待入图谱"段
- 异常处置：报告只读（外部源）→ 仅生成建议清单不回写


## 🔗 关联

- **触发自**：[[logic/]]
- **作用于**：[[stocks/]]
- **执行记录**：[[reviews/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
