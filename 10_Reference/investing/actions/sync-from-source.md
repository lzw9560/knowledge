---
type: action
action_id: SYNC-001
action_type: 链接维护
trigger: 战法卡漂移检测报 drift（vault 战法卡 source_sha ≠ 源仓对应文件当前 SHA）
target: strategies/
audit: true
status: stub
created: 2026-09-07
confidence: high
source: logic_rules
---

> [!info] ⚡ 动作
> **动作**：`SYNC-001`  **类型**：链接维护
> **触发**：`战法卡漂移检测报 drift（vault 战法卡 source_sha ≠ 源仓对应文件当前 SHA）`  **目标**：`strategies/`
>
> **触发自**：[[10_Reference/investing/logic/index|logic/]]

## 📋 动作定义

- **类型**：链接维护（源仓 → vault 增量同步）
- **触发条件**：[[10_Reference/investing/logic/战法卡漂移检测]]（DRIFT-001）报告 drift=true（vault 战法卡 frontmatter 的 `source_sha` ≠ 源仓 `backend/strategies/cards/` 对应文件的当前 SHA）
- **目标实体**：`strategies/`（12 张战法卡）
- **审计**：true（记录同步前后 SHA + diff）


## 🔧 执行步骤

1. 读取 drift 报告，列出所有 drift=true 的战法卡
2. 对每张 drift 战法卡：
   - 从源仓 `backend/strategies/cards/<name>.md` 读取当前正文
   - 比对 vault 战法卡正文 vs 源仓正文（生成 diff）
   - 用源仓正文覆盖 vault 战法卡正文（保留 vault frontmatter，仅更 `source_sha`）
   - 写入新 `source_sha` = 源仓当前 SHA
3. 同步完成后写审计快照到 `reviews/`


## 🔍 审计点

- 执行前状态：vault 战法卡正文 + 旧 source_sha
- 执行后状态：vault 战法卡正文（= 源仓正文）+ 新 source_sha
- 异常处置：源仓文件不存在/读取失败 → 跳过 + 告警


## 🔗 关联

- **触发自**：[[10_Reference/investing/logic/index|logic/]]
- **作用于**：[[10_Reference/investing/stocks/index|stocks/]]
- **执行记录**：[[10_Reference/investing/reviews/index|reviews/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个
