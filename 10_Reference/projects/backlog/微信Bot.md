---
type: project
name: wechat-bot
title: 微信 Bot
status: 待配置
created: 2026-09-07
---

# wechat-bot

## 项目概述
微信消息推送 bot。盘前投研简报 + 盘中异动提醒推送到微信，实现投研结果到手机的最后一公里。

## 状态
- **代码就绪，待配置**：推送逻辑已实现，待配置微信机器人 webhook 与目标群组
- 待办：配置 webhook、配置推送策略（哪些战法触发推送）、合规自查（见下方）

## 技术栈
- 语言：[[10_Reference/tech-learning/languages/python|Python]]
- 集成：[[10_Reference/projects/active/Vibe-Research|Vibe-Research]] 的 [[10_Reference/investing/specs/archive/m0-foundation/S011-调度收口|S011 调度收口]] 调度产出 → 微信推送

## 与 Vibe-Research 的关系
- wechat-bot 是 Vibe-Research 的**输出渠道扩展**
- 推送内容：[[10_Reference/investing/strategies/|战法卡]] 触发信号、[[10_Reference/market_sentiment/情绪仪表盘|情绪看板]] 异动
- 合规边界：推送是**私人决策辅助**，非荐股——遵守 AGENTS.md 弱合规（CLAUDE.md §1）

## 相关链接
- [[10_Reference/reading/MOC]]
- [[10_Reference/investing/MOC]]
- [[10_Reference/projects/active/Vibe-Research]]
- [[10_Reference/reading/MOC]]
- [[10_Reference/meta/四构件本体方法论]]
