---
type: index
layer: active
date: 2026-09-09
description: 多领域专家逐个讨论·active层暂存——未定论前发现/verdict放此，定论后promote到10_Reference/investing/对应文件夹
---

# 专家逐个讨论 · active 层

> 📍 **active 层暂存**——多领域专家逐个讨论的发现/verdict，**未完全定论前都放这儿**（不进 `10_Reference/investing/` reference 层）。某条定论后，promote 到 reference 对应文件夹（metrics/strategies/data-sources/logic/specs）。
>
> 规矩（用户 2026-09-09 定）：每轮专家讨论 = (1) 一份 memory 落 verdict（`~/.claude/projects/-Users-lizhiwei-project-code-stock-Vibe-Research/memory/`）(2) KG active 层写可复用实体（本文件夹）。

## 第 1 轮 · 交易成本会计师（2026-09-09）

verdict memory: `expert-round-cost-accountant-2026-09-09`（10万/没免五/单笔1-4万 → 主仓长线 + gap 卫星≤20%条件性 + 打板搁置）

- [[00_Active/projects/vibe-research/expert-rounds/A股交易成本结构]]（logic 候选）——成本三组件（5元最低佣金+印花0.05%+滑点0.70%往返+T+1）+ 单笔曲线 floor@2万 + 周期分布（超短吃60%+/长线<3%）
- 关联 codebase 硬伤 memory: `gap-edge-cost-never-wired-2026-09-09`（gap 三脚本成本不一致 + accounting.py 5元最低未接线 + 60d robust_edge t/p 没落盘未核实）

## 第 2 轮 · A 股合规监管（2026-09-09，done）

verdict memory: `expert-round-compliance-2026-09-09`（撤回「死局」overclaim；打板 legal if 真买不撤单；§44 核实 0 validated selection edge；候选=尾盘封板 late_lock p=0.012 lift1.33 只差 days；二板 anti 0.95；秒板 anti 0.36；打板不 shelving 但不上仓，track 攒 60d 复验）

- [[00_Active/projects/vibe-research/expert-rounds/A股异常交易监管]]（logic 候选）——证券法 55/56/192 + 虚假申报阈值 + 连板特停偏离值 + 2025 程序化新规
- [[00_Active/projects/vibe-research/expert-rounds/打板形态§44verdict图]]（metric 候选）——recorder.db 83 行打板各形态 lift/p/status 核实图

## 第 5 轮 · 社区开源实践者（2026-09-09，done）

verdict memory: `expert-round-opensource-practitioner-2026-09-09`（用户「都做」→ A 臂指数复制 floor + B 臂 ash-mcp smart-beta experimental capped 30-40%；kill 规则献计：6 月净超额<0+夏普低于指数→砍回 A，熊市暂停；谋士 posture 固化）

- [[00_Active/projects/vibe-research/expert-rounds/红利低波复合因子]]（metric 候选）——A 股长线最硬，三重定论（学术+卖方+指数），年化9-12%回撤<14%熊市逆势+42%
- [[00_Active/projects/vibe-research/expert-rounds/动量因子_A股]]（metric 候选）——A 股动量长期无效，别套美股；反转 IC=0.068/IR=0.447 但 2020 后衰减
- [[00_Active/projects/vibe-research/expert-rounds/zlotus-ash-mcp]]（data_source 候选）——baostock+akshare MCP，自带价值因子评分+低估筛选+再平衡，最对路 fork
- [[00_Active/projects/vibe-research/expert-rounds/qlib]]（data_source 候选）——Alpha158 纯量价无价值因子，纠偏「qlib wrap 价值」误传

## 待办（promote 候选，定论后迁移）

- 用户「都做」启动后，**指数复制臂**（akshare 取 930955 成分+半年调样）跑通 + 红利低波结论定型 → promote [[00_Active/projects/vibe-research/expert-rounds/红利低波复合因子]] 到 `10_Reference/investing/metrics/`
- **ash-mcp 臂**真 clone+wire+跑通 → promote [[00_Active/projects/vibe-research/expert-rounds/zlotus-ash-mcp]] 到 `10_Reference/investing/data-sources/`
- [[00_Active/projects/vibe-research/expert-rounds/A股交易成本结构]] 被多轮引用定型 → promote 到 `10_Reference/investing/logic/`
- [[00_Active/projects/vibe-research/expert-rounds/动量因子_A股]]/[[00_Active/projects/vibe-research/expert-rounds/qlib]] 作为「纠偏/避坑」知识定型后 promote

## 关联

- 全部专家清单（6 位）：交易成本会计师 ✅ / A股合规监管专家 / 数据基建工程师 / 个人投资者实战操盘手 / 社区开源实践者 进行中 / 行为金融交易心理教练
- memory 索引：`MEMORY.md` 里 `expert-round-*` 条目
- reference 层入口：[[10_Reference/investing/MOC]]
