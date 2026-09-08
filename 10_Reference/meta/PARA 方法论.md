---
type: methodology
name: PARA 方法论
domain: 通用知识管理
created: 2026-09-07
source: Tiago Forte《Building a Second Brain》
---

# PARA 方法论

> 领域无关的通用知识组织方法论。本 vault 的 `10_Reference/` 是 PARA 的 Resources 层。

## 核心定义

PARA 把所有信息按"与当前项目的相关度"分四层：

| 层 | 文件夹 | 性质 | 投研 vault 实例化 |
|---|---|---|---|
| **P**rojects | `00_Active/` | 有截止日期的活跃项目 | `00_Active/PROFILE.md`（当前关注领域 + 风格声明）|
| **A**reas | `[[10_Reference/investing/` |长期维护的领域（无截止日期） | 投研知识图谱本体（stocks/strategies/...） |]]
| **R**esources | `[[[[10_Reference/meta/` |跨领域主题资料 | 本文件所在目录（方法论） |]]
| **A**rchives | `20_Archive/` | 完成或废弃的项目 | 已归档 spec / 历史决策 |

## 关键原则

1. **按可行动性而非主题分类**：Projects 是"在做的事"，Areas 是"长期维护的事"，Resources 是"参考素材"，Archives 是"过去的事"。
2. **四层互不重叠**：一个文件只能在一层。投研子区是 Areas 层——它维护"投研知识怎么连"，不是"今天买什么"（那是 Projects）。
3. **时效性递减**：Projects 最活跃（每天动），Areas 次之（每周维护），Resources 静态（很少改），Archives 只读。

## 与本 vault 的对应

- `00_Active/`：活跃项目（交易日志 ora-3 §5.1 应落此，不放 Resources）
- `10_Reference/investing/`：投研领域（Areas 层，本图谱主体）
- `10_Reference/market_sentiment/`：情绪追踪领域（Areas 层，独立子区）
- `10_Reference/meta/`：跨领域方法论（Resources 层，本目录）
- `20_Archive/`：归档（未建）

## 跨领域实例

- [[10_Reference/investing/MOC]] — 投研子区 MOC（Areas 层实例化）
- [[[[10_Reference/meta/MOC 方法论 — MOC 方法论（与 PARA 互补的导航层）]]

## 来源

- Tiago Forte《Building a Second Brain》（2022）
- 详见 multi-project-integration-plan §3 对应讨论
