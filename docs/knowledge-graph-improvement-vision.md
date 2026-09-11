# 投研知识图谱完善愿景（基于实证的诊断与建议）

> **状态**：建议稿（待评审）
> **生成时间**：2026-09-06
> **作者**：Oracle（战略审查）
> **方法论对齐**：`ontology-knowledge-graph` skill 四构件 + Curated 质量门 + 四层推断 + ReAct 审查；`docs/knowledge-graph-llm-pipeline.md`；`docs/multi-project-integration-plan.md`
> **证据基础**：2026-09-06 对 vault（`10_Reference/investing/`、`daily/`、`10_Reference/market_sentiment/`、`scripts/vault_audit.py`、`.github/workflows/`）与源仓（`Vibe-Research/backend/strategies/cards/`、`backend/news_sources.json`、`specs/`）的实际核查。所有数字可复现，非估算。

---

## 目录

0. [先说诊断：五个硬事实推翻一个隐含前提](#0-先说诊断五个硬事实推翻一个隐含前提)
1. [消费层——让图谱每天被用起来](#1-消费层让图谱每天被用起来)
2. [活起来——防止图谱腐化](#2-活起来防止图谱腐化)
3. [深度——从实体关系到洞察](#3-深度从实体关系到洞察)
4. [跨界——投研与其他知识域打通](#4-跨界投研与其他知识域打通)
5. [人性化——贴合个人投研风格](#5-人性化贴合个人投研风格)
6. [开放性——对接外部知识源](#6-开放性对接外部知识源)
7. [建议砍掉或暂缓（YAGNI）](#7-建议砍掉或暂缓yagni)
8. [优先级矩阵](#8-优先级矩阵)
9. [30 天落地路线](#9-30-天落地路线)

---

## 0. 先说诊断：五个硬事实推翻一个隐含前提

提问的六个方向（消费层/活起来/深度/跨界/人性化/开放性）都建立在一个隐含前提上：**「图谱内容是对的，只是缺消费场景和更新机制」**。

核查后这个前提不成立。真实情况是三层问题叠加，且层次之间有依赖：**内容错配 → 入口断开 → 构件残缺**。

### 事实 1：图谱记录的股票与真实关注的股票零重叠

| 来源 | 标的 |
|---|---|
| `stocks/` 11 个实体 | 贵州茅台、五粮液、宁德时代、比亚迪、紫金矿业、中芯国际、长电科技、通富微电、华天科技、光迅科技、中天科技 |
| `daily/2026-09-05_pre_盘前情绪报告.md` Top5 龙虎榜 | 楚天龙(003040)、远东股份(600869)、天娱数科(002354)、国芳集团(601086)、金健米业(600127) |
| 同报告 Top5 热榜 | 国芳集团、楚天龙、金健米业、宇树科技(688836)、蓝色光标(300058) |

**交集 = 0。**

这不是「图谱建错了」——`stocks/` 的 11 只恰好命中 `00_Active/PROFILE.md` 声明的关注领域（半导体/封测/通信/智驾），是按画像静态建的。盘前报告是按**当日情绪热点**动态生成的。两者各自正确，服务不同场景。

但它揭示了一个结构性缺口：**图谱没有「热点股临时入图」的通道**。用户每天真正盯的票，图谱里一只都没有；于是「打开图谱查一下」这个动作每天都没有理由发生。这是「不想打开图谱」的第一根因，比任何消费层设计都更靠前。

### 事实 2：消费入口物理断开（0 个双链）

```
grep -roh '\[\^*\]\]' daily/ | wc -l   →  0
```

- `daily/` 3 份报告（盘前情绪/竞价异动/盘后复盘）：**0 个双链**。
- `10_Reference/market_sentiment/daily/` 5 份报告：29 个双链，**无一指向 `investing/`**。唯一 "investing" 字面命中是页脚的数据源名 `investing.com`。

也就是说：每天自动生成的盘前/盘后报告（已经是成熟产出，含 6 层 z-score、三维向量、仓位建议、三重护栏、对抗性分析），与 71 个实体的知识图谱之间**没有任何一条链接**。

「消费层」不需要新造场景——**最高频的消费场景已经存在（每日两份报告），只是没接上**。这决定了方向 1 的优先级排序。

### 事实 3：四构件缺 2，9 个实体目录是空壳

| 目录 | 文件数 | 状态 |
|---|---|---|
| `actions/` | 1（仅 index.md） | ❌ 构件 4 零内容 |
| `logic/` | 1（仅 index.md） | ❌ 构件 3 零内容 |
| `events/` | 1 | ❌ 空壳 |
| `metrics/` | 1 | ❌ 空壳 |
| `valuations/` | 1 | ❌ 空壳 |
| `dragon-tiger/` | 1 | ❌ 空壳 |
| `reports/` | 1 | ❌ 空壳 |
| `analysts/` | 1 | ❌ 空壳 |
| `indices/` | 1 | ❌ 空壳 |

有内容的只有 5 类：`stocks/`(11) `industries/`(7) `concepts/`(6) `strategies/`(12) `data-sources/`(16) `specs/`(18)。

后果是**图谱最核心的「实体 + 时点数据」组合不成立**。`stocks/600519.md` 写了 5 个 Dataview 查询（财务/估值/研报/龙虎榜/事件），**全部返回空表**，因为 `metrics/` `valuations/` `reports/` `dragon-tiger/` `events/` 里一个实体都没有。个股页打开看到的是 5 个空白表格。

这是「打开图谱没收获」的第二根因：不是没有实体，是**实体之间的关联维度全是空的**。

### 事实 4：审查闭环是假的，且 101 项 high 中 36 项是脚本误报

`reviews/2026-09-06-ci-audit.md`：122 项发现（critical 11 / high 101 / medium 7 / low 3）。文末跟踪清单：

```
- [ ] Critical 全部修复（11）
- [ ] High 修复或进 spec（101）
- [ ] Medium 进 backlog（7）
- [ ] 下次审查日期：下周日
```

**4 个复选框全空。** CI 每周日自动跑、自动 commit 报告（`git log`: `chore: 自动审查报告 2026-09-06`），但报告没有任何消费者。这是「自动化产生报告」而非「自动化驱动改进」——比没有 CI 更危险，因为它制造了「质量在被看护」的错觉。

更关键的是 **101 项 high 的构成**（65 + 36 = 101，恰好全部）：

| 子类 | 数量 | 真实性质 |
|---|---|---|
| `schema_infer` 战法缺字段 | **36** | ❌ **脚本误报** |
| `broken_link` 断链 | **65** | ⚠️ 混合：17 个是部分导入悬空，3 个是模板规划未建目录，其余是 spec 互引 |

**误报证据**：脚本报 `strategies/first_plate.md` 缺 `entry_conditions` / `exit_conditions` / `match_conditions`。但该文件正文里有：

```
## 入场条件
- 基因得分（total_score）≥ 40
- 涨停频次 ≥ 6

## 退出参数
- 止损：跌破入场价 -3%
- 止盈：涨至 +8%（入场价基准）触发减仓锁利
- 最大持有：3 日
```

内容齐全，只是写在正文而非 frontmatter。`scripts/vault_audit.py:388` 的 `schema_infer` 只比对 frontmatter 字段，不读正文。**12 张战法 × 3 字段 = 36 条噪声**，占 high 级 36%。

**断链的真实成因**（不是错链）：

```
vault 已有 spec：13 个（S007 S008 S010 S011 S017 S018 S019 S020 S031 S047 S066 S094 S100）
被 [[]] 引用的 spec：29 个
被引用但不存在：S004 S006 S009 S013 S015 S023 S030 S032 S041 S042 S049 S064 S075 S086 S097 S101 S102（17 个）
```

源仓有 60 个 spec，vault 只导入了 13 个，而导入的这 13 个在正文里互相引用了 16 个未导入的编号。这是**部分导入的必然结果**，不是图谱错误。另 3 条断链（`` `` ``）是模板设计时规划了目录但未建。

含义：**修脚本 + 定规则的成本远低于补 101 个实体**。当前 high 级噪声淹没了真问题，导致「反正修不完」→ 复选框全空。

### 事实 5：战法卡是源仓正文的逐字拷贝

```
diff <(cat backend/strategies/cards/first_plate.md) \
     <(cat vault/.../strategies/first_plate.md)
→ 0a1,8  （vault 版仅多出 8 行 frontmatter，正文 0 差异）
```

12 张战法卡全部如此。两个问题：

1. **自我矛盾**：`MOC.md:120` 明写「本 vault 不复制代码逻辑，只做知识表征」，实际却逐字拷贝了源仓正文。
2. **同步漂移定时炸弹**：源仓 `cards/*.md` 一改，vault 立刻过时，且**无任何检测机制**（审查脚本不比对源仓）。`specs/S100-战法卡片对齐.md` 这个 spec 名字本身说明战法卡还在演进中。

### 附：三项设计已落地但实现缺位

| 设计文档承诺 | 实现状态 |
|---|---|
| `.entity-dictionary.json`（pipeline §2，链接一致性的核心） | ❌ **文件不存在**。而事实 4 的 17 个 spec 悬空恰恰是词典要解决的问题 |
| MCP 集成（pipeline §7，8 个工具） | ❌ **未配置**（`~/.config/opencode/opencode.json` 无 obsidian 命中）。`docs/obsidian-mcp-setup.md` 写了但没执行。「AI 对话直接查图谱」当前不可行 |
| newsradar 108 源 → 抽取进 inbox（方向 6 设想） | ⚠️ 108 源中**仅 3 个**是 A股/财经（华尔街见闻、东方财富股票、东方财富资讯），其余是 OpenAI / Google Research / Hugging Face / 量子位 / MIT Tech Review AI。12 个 industries 是科技产业分类（AI/半导体/机器人），非 A股行业。**源结构与投研抽取不匹配** |

### 诊断结论：优先级必须重排

提问的顺序（消费层 → 活起来 → 深度 → 跨界 → 人性化 → 开放性）隐含「先做消费层」。但实证显示：

```
内容错配（事实1、3）  ← 根因，不修则消费层接了也是空的
      ↓
入口断开（事实2）    ← 最高 ROI 的修复点，因为报告已存在
      ↓
构件残缺（事实3）    ← 与事实1同源，需要事件/指标实体填充
      ↓
审查失真（事实4）    ← 放大器：让上面三个问题看不见
      ↓
拷贝漂移（事实5）    ← 慢性，但会持续侵蚀信任
```

**重排后的第一性原则**：

> 图谱的价值 = （实体与用户真实决策的相关度）×（消费入口的触达频率）×（关联维度的填充度）
>
> 当前三项分别约为：低（0 重叠）× 零（0 双链）× 低（5/14 类有内容）。乘积接近 0。
>
> 所以**先修乘数中最小的一项**——消费入口触达频率（从 0 到 1 是无穷倍提升，且成本最低，因为报告已经每天在生成）。

---

## 1. 消费层：让图谱每天被用起来

### 1.1 【P0】盘前/盘后报告模板注入「图谱关联段」

**价值**：★★★★★
**难度**：低
**依赖**：无

这是全案 ROI 最高的一项。理由：报告**已经每天自动生成**（`daily/` 3 份 + `market_sentiment/daily/` 5 份），内容已经成熟（6 层 z-score / 三维向量 / 仓位建议 / 三重护栏 / 对抗性分析 / 熔断状态），**只差链接**。从 0 双链到每份报告 5-10 个双链，不需要新建任何场景。

**落地路径**：

1. 定位报告生成器（`Vibe-Research` 后端的盘前报告生成逻辑，参见 `docs/premarket-workflow-logic.md`）。
2. 在报告的「🎯 关注方向」与「Top5 龙虎榜/热榜」两处，对每个出现的股票代码做一次 vault 查询：
   - **命中已有实体** → 输出 `贵州茅台` 双链 + 一行摘要（行业/已关联战法数）。
   - **未命中** → 输出裸代码 `楚天龙(003040)`，并在报告末尾「图谱缺口」段追加一行：`- [ ] 003040 楚天龙 未入图谱`（这直接喂养 1.3）。
3. 报告末尾固定追加「📚 图谱关联」段：
   ```markdown
   ## 📚 图谱关联
   - 本报告涉及个股：N 只，其中 M 只已在图谱（M/N）
   - 关联战法：first_plate dragon_head
   - 图谱缺口：见下方待办
   - [ ] 003040 楚天龙 未入图谱
   ```

**验收**：连续 3 个交易日生成的报告，双链数 > 0 且「图谱缺口」清单非空（说明触达在起作用）。

**关键设计点**：第 2 步的「未命中 → 追加待办」是整套机制的发动机。它把「图谱与热点零重叠」这个静态缺陷，转化为**每天自动产生的、有具体标的的入图待办**。不需要人工想「该往图谱里加什么」。

### 1.2 【P0】修复 `matched_strategies` 死查询，打通战法↔股票双向边

**价值**：★★★★★
**难度**：低
**依赖**：无

**问题**：`templates/strategy.md` 第 29-36 行定义了图谱里最高价值的查询：

```dataview
TABLE code AS "代码", name AS "名称", industry AS "行业"
FROM "stocks"
WHERE type = "stock" AND contains(matched_strategies, this.name)
```

但核查 `stocks/*.md` 的 frontmatter 字段（`type` `code` `name` `market` `industry` `concept` `list_date` `st` `pe_ttm` `pb` `market_cap` `created`）——**没有任何一个实体有 `matched_strategies` 字段**。这个查询永久返回空表。

反向：`stocks/600519.md` 正文有 2 条手工战法链接（`low_absorption`、`dragon_head`），但 `strategies/*.md` 正文里**没有一个 `stocks/` 链接**（只有 `strategies/index.md` 有）。

后果：「这张战法历史上匹配过哪些票」——投研里最高频的问题之一——在图谱里问不出来。

**落地路径**（二选一，推荐 A）：

- **方案 A（正边，推荐）**：给 `stocks/*.md` frontmatter 补 `matched_strategies: [low_absorption, dragon_head]`。数据源现成——正文里已有手工链接，写个 10 行脚本把正文的 `xxx` 提取到 frontmatter。
  - 优点：Dataview 的 `contains()` 直接可用，模板查询零改动。
  - 成本：11 个文件，脚本化 5 分钟。
- **方案 B（反边）**：靠 Obsidian 反向链接面板，不加字段。
  - 否决理由：反链面板只显示「谁链了我」，不支持 `WHERE industry = "白酒"` 这类条件聚合，无法做「半导体封测板块里匹配 dragon_head 的票」这种真问题。

**验收**：`strategies/dragon_head.md` 打开后「匹配股票」表格非空。

### 1.3 【P0】热点股 30 秒入图通道（inbox stub）

**价值**：★★★★★
**难度**：中
**依赖**：1.1（缺口清单是其输入）

这是修复**事实 1（零重叠）**的唯一手段。图谱不含用户当天盯的票，所以图谱永远不会被打开。

**设计**（严格复用 pipeline §5 已有的 stub 机制和 inbox 质量门，不另起炉灶）：

1. **输入**：1.1 产出的「图谱缺口」清单（每日自动累积）。
2. **触发**：手动 QuickAdd 命令（插件已装）或脚本批量。
3. **动作**：按 `templates/inbox-item.md` 生成最小 stub 到 `inbox/`：
   ```yaml
   ---
   type: stock
   code: 003040
   name: 楚天龙
   confidence: medium
   source: "daily-report:2026-09-05"
   quality_score: 40
   approved: false
   created: 2026-09-05
   ---
   ```
   正文只留一行「> 由盘前报告缺口自动建档，待补充核心业务/战法关联」。
4. **字段来源**：调用 `Vibe-Research` 已有的 `astock.py:individual_info()`（pipeline §2 已指定此源），取名称/行业/上市日/是否ST。**不调 LLM**——这是 L1 规则抽取，confidence 可给 medium 而非 low。
5. **晋级**：`quality_score` ≥ 60 且有 ≥1 条战法或行业边 → `mv` 到 `stocks/`，加 `approved_date`。这一步可以是每周日 CI 审查时顺带做（复用已有 workflow）。

**关键纪律**（避免 inbox 变垃圾场）：

- stub **只建图谱里会被反复引用的实体**。一次性出现在龙虎榜、次日再不出现的票，不建。判据：`inbox/` 里同一 code 被 ≥2 份不同日期报告命中才建档。这条写进 `logic/`（顺便填充构件 3，见 3.1）。
- inbox 滞留 > 14 天未晋级 → 自动标 `rejected: true` + `reject_reason: 未达引用阈值`，季度清理。

**验收**：2 周后 `stocks/` 实体数从 11 增长，且新增实体与盘前报告 Top 榜有实际重叠（重叠率 > 30%）。

### 1.4 【P1】MCP 真正配起来（设计已有，执行缺位）

**价值**：★★★★
**难度**：中
**依赖**：1.2、1.3（否则 MCP 查出来也是空表）

`docs/obsidian-mcp-setup.md` 已写好配置，`knowledge-graph-llm-pipeline.md` §7 已列 8 个工具的用途，但 `~/.config/opencode/opencode.json` 里**无 obsidian MCP 条目**。提问中「帮我查白酒行业所有股票的 PE 排序 → MCP 查 Dataview」这个场景当前**不可实现**。

**落地路径**：

1. 按 `docs/obsidian-mcp-setup.md` 执行安装，起步用 `yanxue06/obsidian-mcp`（25 工具）。
2. **先验证 3 个高频查询能跑通**，再谈扩展：
   - `query_dataview('TABLE name, pe_ttm FROM "stocks" WHERE industry = "白酒" SORT pe_ttm ASC')`
   - `find_broken_links()` — 与 `scripts/vault_audit.py` 结果交叉验证（两个实现互查，能发现脚本 bug，如事实 4 的误报）
   - `traverse_graph("stocks/600519", depth=2)` — 影响范围分析
3. 在 `AGENTS.md` 的「会话开始协议」里加一条：会话中遇到个股/战法/数据源问题，**先 `query_dataview` 再回答**，不凭记忆。这把 MCP 从「可用」变成「默认用」。

**注意**：`pe_ttm: 25.0` / `pb: 8.0` / `market_cap: 2.1T` 这类 frontmatter 值，`stocks/600519.md:42` 自己标注了「为公开常识值，待实时更新」。**MCP 查出来的 PE 是不可信的静态值**。所以第 2 步的 PE 查询要么先接实时源（见 2.5），要么明确标注数据时点。不臆造数据是 `AGENTS.md` 的工程底线，不能让 MCP 成为臆造数据的放大器。

**验收**：在 opencode 会话里问「白酒行业有哪些股票」，agent 走 MCP 返回而非凭记忆。

### 1.5 【P2→砍】前端「图谱关联节点数」徽标

**价值**：★★
**难度**：高
**建议**：**暂缓，不进 30 天计划**

理由：

- 跨系统耦合（vault 是 Obsidian markdown + GitHub 私有仓，前端是 FastAPI+React），需要 vault 导出 API 或构建产物，工程量与其余 4 项不在一个量级。
- 当前节点数本身没有信息量——事实 3 显示 `metrics/` `valuations/` `events/` 全空，茅台的「关联节点数」现在只有行业+概念+数据源，徽标会显示一个很小的数字，**反而暴露图谱的贫瘠**，降低打开意愿。
- 消费频率错配：前端是个股页，用户在前端看盘；图谱是研究沉淀，用户在 Obsidian 里做研究。两者不是同一心智场景。

**替代方案**（成本近零，价值更高）：在 `Vibe-Research` 个股页加一个「📖 在知识图谱中查看」外链，跳 `obsidian://open?vault=...&file=stocks/600519`。Obsidian URI scheme 原生支持，一行 `<a>` 标签。这实现了「从工作流跳到图谱」的单向通路，不需要任何数据同步。

---

## 2. 活起来：防止图谱腐化

### 2.1 【P0】审查报告 → 可执行工单（闭合假闭环）

**价值**：★★★★★
**难度**：低
**依赖**：2.2（先降噪，否则工单全是噪声）

事实 4 显示 122 项发现、4 个复选框全空。**报告没有消费者，就不算审查**。

**落地路径**（对齐 `AGENTS.md` 已有的 `.scratch/` issue tracker 机制，不新造）：

1. `scripts/vault_audit.py` 末尾增加输出：把 critical/high 发现写成 `.scratch/kg-audit/issues/NN-<slug>.md` 工单（`AGENTS.md` 已定义此目录为 medium 级 code review 的工单层），每条含：发现类型 / 实体路径 / 修复动作 / 建议责任方（脚本修 or 人工补 or 规则豁免）。
2. `reviews/<date>-ci-audit.md` 的跟踪清单改为**指向工单**，而非裸复选框：
   ```markdown
   - [ ] Critical（11）→ 见 .scratch/kg-audit/map.md#critical
   - [x] High 中 36 项 schema 误报 → 已由脚本修复关闭（commit xxx）
   ```
3. **每周审查报告必须有一个「本期关闭」段**，记录上周工单的处理结果。没有关闭记录的审查 = 无效审查。

**纪律**（这是「活起来」的核心）：审查报告的 KPI 不是「检出多少」，是「**关闭多少 + 剩余多少**」。当前脚本只统计前者，所以数字只会单调增长（122 → 下周 130 → 再下周 145），最终没人看。

**验收**：下一份周日报告的「本期关闭」段非空，且 `findings_count` 环比下降。

### 2.2 【P0】修审查脚本：消除 36 项误报 + 断链分级

**价值**：★★★★★
**难度**：低
**依赖**：无

这是 2.1 的前置——**先降噪才能闭环**。不修脚本，101 项 high 永远修不完，复选框永远空着。

**三处修改**：

**(a) `schema_infer` 读正文，不只读 frontmatter**（消除 36 项误报）

`scripts/vault_audit.py:388` 的 `schema_infer` 当前只比对 frontmatter 键。改为**二级判定**：

```
字段缺失判定：
  frontmatter 有该键        → 通过
  frontmatter 无，但正文有对应 H2 标题（如 entry_conditions ↔ "## 入场条件"）
                            → 通过，标 "body_only"（low 级提示，建议提升到 frontmatter 以便 Dataview 查询）
  两者都无                  → 才报 high
```

实现：加一个 `FIELD_TO_HEADING` 映射表（`entry_conditions: ["入场条件", "入场", "Entry"]`）。约 20 行代码。

**附带收益**：`body_only` 这个 low 级提示是有用信号——它指出「内容存在但不可查询」。战法正文有入场条件，但 Dataview 查不出来，这正是 1.2 那类死查询的根源。

**(b) 断链分级：区分「错链」与「未导入」**（65 项 → 真实错链可能 < 10 项）

当前 65 条断链一律报 high。但成因不同，处置不同：

| 断链类型 | 判据 | 应报级别 | 处置 |
|---|---|---|---|
| **未导入悬空** | 目标是 `specs/SNNN`，源仓存在该 spec 但 vault 未导入 | low（已知缺口） | 计入「导入进度」，不算缺陷 |
| **目录规划未建** | 目标是 `news/` `macro/` `sectors/`，模板引用但目录不存在 | medium | 二选一：建目录 or 改模板（见 2.4） |
| **真错链** | 目标在任何源都不存在 | high | 必须修 |

实现：断链检测时多查一次源仓 `specs/` 目录列表（`ls /Users/lizhiwei/project/code/stock/Vibe-Research/specs/`），能区分前两类。

**效果预估**：17 个 spec 悬空降为 low，3 个目录断链降为 medium，high 级断链从 65 降到个位数。**high 从 101 → 约 10**，这才是可闭环的量级。

**(c) `coverage` 的 critical 判据加「是否规划」**

当前 11 项 critical 全是「实体类型数量为 0」。但 `audit` 类型为 0 是正常的（审查报告本身 `type: audit`，只是被 `WHERE file.name != ...` 排除了——这是脚本自己的统计口径 bug）。改为：critical 只报**四构件核心类型**（logic / action）为 0，其余类型报 medium。

理由：`logic` 和 `action` 为 0 是**方法论缺陷**（四构件缺 2，见 3.1），确实 critical；`analyst` 为 0 只是「还没导入研报」，是进度问题不是结构问题。

### 2.3 【P1】战法卡去副本化：从「拷贝正文」改为「源指针 + 漂移检测」

**价值**：★★★★
**难度**：中
**依赖**：无

事实 5：12 张战法卡是源仓正文逐字拷贝，违反 `MOC.md:120` 自定原则，且无漂移检测。

**落地路径**：

1. **vault 战法实体只保留三块**：frontmatter（结构化字段，供 Dataview 查询）+ 「图谱关联」段（`stocks/` `events/` 等真实知识边）+ **源指针**。正文逻辑段删除，替换为：
   ```markdown
   # 战法逻辑
   > 源文件：`Vibe-Research/backend/strategies/cards/first_plate.md`（单一真相源）
   > 源仓 sha：`a1b2c3d`（导入时记录）
   > 用 Obsidian 打开源文件：本地链接
   ```
   或者用 `!...` embed 直接嵌入源文件内容（Obsidian 支持 vault 外路径需配置，或用符号链接）。
2. **漂移检测进审查脚本**（第 9 项检查）：比对 vault frontmatter 里记录的 `source_sha` 与源仓 `git rev-parse HEAD:backend/strategies/cards/first_plate.md`。不一致 → 报 medium「源已变更，vault 待同步」。
3. **结构化字段进 frontmatter**（顺便修掉 2.2(a) 的 body_only）：把正文的入场/退出条件提取为 frontmatter：
   ```yaml
   match_conditions: ["基因得分≥40", "涨停频次≥6"]
   exit_conditions: ["止损-3%", "止盈+8%", "最大持有3日"]
   ```
   这才是 vault 该做的事——**把非结构化正文变成可查询的结构化字段**，而不是拷贝正文。

**收益**：① 消除漂移风险（源仓改了立刻被检出）；② 战法条件变成 Dataview 可查（「所有止损严于 -3% 的战法」）；③ 符合自定原则；④ vault 体积下降。

**同类处理**：`specs/` 18 个实体是否也是拷贝？需同样核查（本次未逐一 diff，建议在 2.3 执行时一并检查）。

### 2.4 【P1】实体词典落地（pipeline §2 已设计，文件不存在）

**价值**：★★★★
**难度**：中
**依赖**：2.2（词典能顺便解决断链分级）

`knowledge-graph-llm-pipeline.md` §2 设计了 `.entity-dictionary.json`，明确「词典是链接一致性的核心——贵州茅台/茅台/600519/Moutai 必须归一到同一文件」。**该文件不存在**。

而事实 4 的断链问题，本质就是缺词典：`S004` 该指向哪里？没有词典就无法判断「这是未导入还是真错链」。

**落地路径**（按 pipeline §2 的设计实现，不修改设计）：

1. **初始化**：扫 vault 现有 70 个实体的 frontmatter（`code` / `name` / `number`）+ 源仓 `specs/README.md` 的 60 个 spec 编号表 + `astock.py:individual_info()` 的股票列表 → 生成 `10_Reference/investing/.entity-dictionary.json`。
2. **关键增量**：词典里为**源仓存在但 vault 未导入**的实体标记 `"status": "not_imported"`。这样断链检测能立刻区分 2.2(b) 的三种类型。
3. **消费方**：① `vault_audit.py` 断链分级；② 未来的抽取脚本（pipeline P2-P5）建链前查词典；③ MCP 的 `query_dataview` 之外的别名解析。
4. **git 追踪**（pipeline §2 已指定），各设备同步。

**附带决策**：`` `` `` 三个目录——建还是不建？

建议**不建，改模板**。理由：`news/` 与 `events/` 语义重叠（MOC.md 第 20 行 `events/` 已定义为「新闻/公告/涨停，对应 News + Announcement + ZTPoolItem」），建 `news/` 会制造两套并行分类。把 `data-sources/cninfo.md` 等 3 个文件里的 `` 改为 `events/`，`` 改为新建的 `macro/`（FRED/worldmonitor 的宏观数据确实无处安放，这个该建）或并入 `indices/`。`` 改 `industries/`（akshare.md 里的历史遗留命名）。

### 2.5 【P2】时效性：用「最后验证日期」替代「置信度衰减」

**价值**：★★★
**难度**：中
**依赖**：1.4（实时数据源接入）

提问设想「长期未验证的实体 confidence 下降」。建议**不做衰减算法**，改为更简单且更可执行的机制。

**否决衰减算法的理由**：

- confidence 在 pipeline §4 里的语义是**抽取可靠度**（L1 规则=high / L3 别名=medium / L4 LLM 语义=low），是「这条数据怎么来的」，不是「这条数据有多新」。把时间衰减混进 confidence 会让一个字段承载两个正交语义，后续无法区分「LLM 猜的」和「很久没更新的」。
- 衰减需要定时重算全库，且衰减速率是拍脑袋参数（30 天？90 天？）。`AGENTS.md` 明确要求「参数选择必须有数据支撑，不得凭直觉拍脑袋」——衰减速率无法给出数据支撑。

**替代方案**：

1. frontmatter 增加两个正交字段：
   ```yaml
   confidence: high              # 抽取可靠度（不变，语义纯化）
   last_verified: 2026-09-06     # 最后一次人工/脚本核验日期
   data_asof: 2026-09-06         # 时点数据的数据日期（pe_ttm 等）
   ```
2. **`stale_check` 用 `last_verified`**（脚本已有 stale_check，当前报「90+ 天未更新实体数：0」——因为所有实体都是 09-06 建的，这个检查现在无意义，3 个月后才有意义）。
3. **时点数据的处置分两类**：
   - `pe_ttm` / `pb` / `market_cap`（`stocks/600519.md:42` 自标「公开常识值，待实时更新」）→ **从 frontmatter 删除**，改为 Dataview 查 `valuations/` 实体（模板已经这么设计了，只是 `valuations/` 是空的，见 3.4）。frontmatter 里放静态常识值 + 让 MCP 查出来当实时值用 = 臆造数据，违反工程底线。
   - `industry` / `list_date` / `st` → 保留，这些真的很少变，配 `last_verified` 即可。
4. **用户行为驱动更新**（提问的设想）：可行且低成本——1.1 的报告生成时，若命中图谱实体且其 `last_verified` > 30 天，在报告「图谱关联」段追加 `- [ ] 600519 贵州茅台 财务数据 45 天未核验`。**复用 1.1 的缺口清单机制**，不需要新基础设施。

---

## 3. 深度：从实体关系到洞察

### 3.1 【P0】填充 `logic/`：把已有的隐式规则显式化（四构件补全）

**价值**：★★★★★
**难度**：中
**依赖**：无

四构件缺 2（事实 3），其中 `logic/` 是**当前最该补的一个**——因为它不需要外部数据，规则已经在项目里存在，只是没被写下来。

`logic/index.md` 自己定义了 4 类规则（校验/状态机/推断/自动化），并明确「规则要可机器执行，不是描述性文字」。**当前 0 条**。

**落地路径**：把本诊断中已经发现的规则直接写成 `logic/` 实体。这批规则的来源是实证，不是臆造：

| 规则文件 | rule_type | 内容 | 来源 |
|---|---|---|---|
| `logic/inbox-promotion.md` | 状态机 | stub 在 inbox 滞留 > 14 天未晋级 → rejected；同一 code 被 ≥2 份不同日期报告命中才建档 | 1.3 的纪律 |
| `logic/stub-trigger.md` | 自动化 | 盘前报告出现图谱未收录代码 → 追加「图谱缺口」待办 | 1.1 第 2 步 |
| `logic/schema-body-fallback.md` | 校验 | frontmatter 缺字段但正文有对应 H2 → body_only（low），不报 high | 2.2(a) |
| `logic/broken-link-grading.md` | 校验 | 断链按「未导入 / 目录未建 / 真错链」三级分流 | 2.2(b) |
| `logic/source-drift.md` | 校验 | vault 战法/ spec 的 `source_sha` ≠ 源仓 → 报漂移 | 2.3 第 2 步 |
| `logic/static-value-ban.md` | 校验 | frontmatter 禁止放时点数据（PE/PB/市值），必须走 `valuations/` 实体 | 2.5 第 3 步 |

**每条规则用 `templates/logic.md`，且必须可机器执行**——即 `vault_audit.py` 里有对应的检查函数。规则写完但脚本没实现 = 文档而非规则。

**收益**：① 四构件从 2/4 到 3/4；② 11 项 critical 中至少 1 项（logic 为 0）关闭；③ **审查脚本的规则从「硬编码在 Python 里」变成「vault 里可读可审的实体」**——这是知识图谱对自己基础设施的反哺，符合 skill 的方法论自洽性。

### 3.2 【P1】`actions/` 填充：构件 4

**价值**：★★★
**难度**：低
**依赖**：3.1

`actions/index.md` 定义为「CRUD / 状态流转 / 链接维护 / 审计快照」。当前 0 条。

落地：把已有动作显式化——`actions/promote-from-inbox.md`（inbox → 正式区的 mv + 加 approved_date）、`actions/weekly-audit.md`（CI 周日审查）、`actions/sync-from-source.md`（源仓 → vault 增量同步，pipeline P5）。

**难度低的原因**：这些动作已经在跑（CI workflow、人工 mv），只是没被记录为实体。写下来即可，顺便发现「哪些动作其实没有执行者」。

### 3.3 【P1】因果 vs 相关：关系谓词加 `kind` 维度

**价值**：★★★★
**难度**：中
**依赖**：3.1

`MOC.md:38` 定义了 10 个关系谓词（`belongs_to` / `tagged` / `covered_by` / `has_metric` / `valued_at` / `involves` / `affects` / `matches` / `authored_by` / `triggered_by`），但**全是平面的**，不区分因果与相关。

投研的核心价值恰恰在这个区分：「白酒行业 PE 分位低」与「白酒行业 PE 分位低 **导致** 资金流入」是完全不同的断言。

**落地路径**：

1. 谓词分三类（写进 `logic/relation-taxonomy.md`）：
   | kind | 谓词 | 含义 |
   |---|---|---|
   | `structural` | `belongs_to` `tagged` `authored_by` `has_metric` | 分类/归属，客观可验证，无需置信度 |
   | `causal` | `affects` `triggered_by` | 因果断言，**必须带 evidence + confidence** |
   | `correlational` | `matches` `covered_by` `involves` | 相关/共现，标观察窗口 |
2. **`causal` 边的强制约束**（写进 `logic/`，由审查脚本执行）：
   ```yaml
   relation: affects
   kind: causal
   direction: 政策放松 → 资源股
   evidence: "daily/2026-09-05_pre:L1 政策层「PPI 上行+CPI 低位=利好资源股」"
   confidence: medium
   sample_size: null        # 无统计支撑则为 null
   exploratory: true        # AGENTS.md：样本 <30 标「探索性」
   ```
3. **对齐 `AGENTS.md` 的「数据支撑优先」底线**：该条明确要求「随机基准必须显式计算，提升不足 2x 的关联视为噪声，不得作为设计依据」。所以 `causal` 边若无 `sample_size` 或 lift < 2x，审查脚本报 high，强制标 `exploratory: true`。

**这是图谱从「记录」升级到「论证」的关键一步**，也是与通用 PKM 的核心差异——投研知识图谱的价值在于**可追溯的因果断言**，不在于节点数。

### 3.4 【P2】`events/` + `metrics/` + `valuations/` 填充（时间线与洞察的物质基础）

**价值**：★★★★★（但难度高）
**难度**：高
**依赖**：1.3（入图通道）、2.5（时点数据规范）

提问的「时间线视图」「反事实推理」「隐藏关联」**全部依赖事件实体**。`events/` 为 0 → 三个设想都没有物质基础。所以这不是「深度」问题，是「构件残缺」问题（事实 3），必须先填。

**落地路径**（分三步，不要一次做完）：

1. **先做 `valuations/`（最易）**：MOC.md 已定义对应 Pydantic 契约 `Valuation` + `ValuationPercentile`，源仓有现成数据。脚本化：对 `stocks/` 11 只各生成一个估值快照实体。**顺便解决 2.5 的 PE 臆造问题**（frontmatter 的静态 PE 删掉，改查 valuations）。
2. **再做 `events/`（中等）**：数据源是 `News` + `Announcement` + `ZTPoolItem` 三个已有契约。但注意——**不要全量导入历史事件**（会产生几千个实体，淹没有价值的）。只导入「图谱里已有股票的、最近 90 天的、涨停/公告类」事件。
3. **`metrics/` 最后做（最难）**：财务数据周期性强、字段多、口径复杂，且 `AGENTS.md` 要求「跨数据源的比较必须先验证数据口径一致性」。建议等 1、2 跑顺再说。

**时间线视图**（`events/` 有了之后）：用 Dataview 而非插件：
```dataview
TABLE date AS "日期", event_type AS "类型", summary AS "摘要"
FROM "events"
WHERE contains(codes, "600519")
SORT date ASC
```
`stocks/600519.md:80` **已经写了这个查询**，只是 `events/` 是空的。填数据即可，不需要新设计。

### 3.5 【P2】轻量图算法：中心性 + 路径，用脚本算、结果写回

**价值**：★★★
**难度**：中
**依赖**：3.4（节点太稀疏时算法无意义）

提问问「哪些图算法适合 Obsidian/轻量级实现」。答案：**度中心性 + 最短路径，两个就够，且必须在节点密度达标后才有意义**。

**现状警告**：事实 2 的链接统计显示，入边 Top3 是 `stocks/index.md`(38) / `events/index.md`(29) / `data-sources/eastmoney-push2.md`(28)。**前两个是目录索引文件，不是真实知识 hub**。审查脚本的 `relation_density` 检查把 `stocks/index.md` 报为「入边异常多」，这是**把模板生成的目录链接误判为知识 hub**——又一个脚本判据问题（应排除 `index.md`）。

所以：

1. **先修判据**：`relation_density` 排除所有 `index.md` / `MOC.md` / `README.md`。修完后真实 hub 只有 `data-sources/eastmoney-push2.md`（28 入边，这是真的——东财确实被大量 spec 引用）。
2. **再加算法**（`vault_audit.py` 第 10、11 项检查）：
   - **度中心性**：排除 index 后，入边 Top10 = 真实知识枢纽。投研含义：「哪个数据源被最多 spec 依赖」→ 单点故障风险；「哪个战法被最多股票匹配」→ 主力战法识别。
   - **最短路径**：给定两个实体，输出连接链路。投研含义：「茅台 ↔ 首板战法 有没有关联路径」→ 若有，路径上的中间节点就是隐藏关联（提问设想的「A、B 都连到 C」）。
   - **实现**：Python `networkx`，解析 `` 建图，约 50 行。结果写回 `reviews/<date>-graph-metrics.md`。**不引入 Neo4j**（pipeline §9 已明确否决重栈，这个决策正确，保持）。
3. **社区发现（Louvain）暂缓**：当前 70 节点、真实边稀疏（事实 2），社区发现会退化成一堆单点。等实体数 > 200 且边密度达标再说。

### 3.6 【P2→暂缓】反事实推理

**价值**：★★★（理论）/ ★（当前可执行性）
**难度**：高
**建议**：**暂缓**，写进 backlog 但不进路线

理由：

- 依赖 `causal` 边（3.3）+ 充足的事件实体（3.4）+ 传播算法。三个前置全部未完成，且 3.4 难度高。
- 「如果某政策出台，哪些实体受影响」这个查询的前提是图谱里有**带方向和强度的因果边**。当前 10 个谓词里只有 `affects` / `triggered_by` 勉强算因果，且**一条实例都没有**（事实 3：`logic/` 空，因果关系从未被建模）。
- 在因果边为 0 的图上做反事实传播，输出的是噪声，且会被误信为洞察——这比不做更危险，违反 `AGENTS.md`「不臆造数据」。

**前置条件**（满足后再启动）：`causal` 边 ≥ 30 条且 ≥ 50% 带 `sample_size`；`events/` ≥ 100 个实体。

---

## 4. 跨界：投研与其他知识域打通

### 4.1 【P0】`market_sentiment` ↔ `investing` 互链（两个孤岛，最高价值跨界）

**价值**：★★★★★
**难度**：低
**依赖**：无

提问设想「投研与技术学习/读书打通」。但核查发现：**vault 里已经存在一个成熟的第二投研子区，与 `investing/` 零互链**。这是比「跨到读书」更近、更有价值的跨界。

`10_Reference/market_sentiment/` 的实际内容：

| 组成 | 状态 |
|---|---|
| `DASHBOARD.md` | ✅ 成熟：6 层稳健 z-score（Median+MAD）、三维向量（温度 Z / 速率 ΔZ / 背离度 D）、仓位映射表（5 档）、护栏（单票≤25%/总仓≤90%/现金≥10%/杠杆≤1.0/止损-7%/日亏≤3%）、熔断等级 |
| `daily/` | ✅ 5 份盘前/盘中报告 |
| `scores/` | ⚠️ 1 份 |
| `reviews/` | ✅ 3 份 |
| `_templates/` | ✅ 6 个 |
| `sentiment/` `policy/` `_graphs/` | ❌ 空 |
| **指向 `investing/` 的链接** | ❌ **0** |

而 `daily/2026-09-05_pre_盘前情绪报告.md` 的内容（机构净买入 -7.64 亿 / 游资 +16.84 亿 / 分歧度 100% / 涨停 38 只 / 连板天梯断层 / IF 基差 -0.35% / 三维向量 Z=+0.1210 ΔZ=+0.2746 D=0.6593）**与图谱里的 12 张战法完全应该关联但没有**：

- 战法卡里有「适用天气」字段（`first_plate.md`: 「阴天（市场情绪偏弱但有个股机会）」）
- 情绪报告里有温度 Z 和仓位建议
- **「阴天」对应哪个 Z 区间？没有任何文件定义这个映射**

这是一个**已经存在、双方都已建好、只差一条链接**的高价值缺口。

**落地路径**：

1. **建「情绪天气 ↔ 战法适用性」映射实体**（这是 `logic/` 的推断规则，同时填 3.1）：
   ```markdown
   # logic/sentiment-weather-mapping.md
   ---
   type: logic
   rule_type: 推断规则
   target_entity: strategy
   severity: high
   ---
   | 天气 | 温度 Z 区间 | 背离度 D | 推荐战法 | 禁用战法 |
   |---|---|---|---|---|
   | 晴 | Z > 1.5 | D < 0.3 | consecutive_relay dragon_head | low_absorption |
   | 阴 | -0.5 ~ 0.5 | 任意 | first_plate low_absorption | consecutive_relay |
   | 雨 | Z < -1.5 | D > 0.6 | pattern_reversal storm_reversal | 全部动量类 |
   ```
   **注意**：这张表的 Z 区间阈值**必须有回测数据支撑**（`AGENTS.md`「数据支撑优先」）。源仓有 `specs/S031-调度收口盘前多层按战法回测.md` 和 `specs/S047-基因分权重回测校准.md`——先查这两个 spec 的回测结论，有数据就填数据，没数据就标 `exploratory: true`。**不要凭直觉填阈值。**
2. **盘前报告注入天气判定 + 战法推荐**（复用 1.1 的模板改造）：
   ```markdown
   ## 🌤️ 图谱战法匹配
   当前天气：阴（Z=+0.1210，D=0.6593）
   → 适用：first_plate low_absorption
   → 禁用：consecutive_relay（背离度过高）
   依据：sentiment-weather-mapping
   ```
3. **反向**：每张战法卡的「适用天气」段改为链接 `sentiment-weather-mapping`，不再各自用自然语言描述「阴天」（12 张卡各写各的，无统一定义 = 不可执行）。

**这一项同时解决 4 个问题**：① 两孤岛连通；② `logic/` 构件填充（3.1）；③ 12 张战法的「适用天气」从模糊描述变成可执行规则；④ 盘前报告增加图谱消费点（1.1）。

### 4.2 【P2】跨领域链接：读书 / 技术学习

**价值**：★★★
**难度**：中
**依赖**：4.1（先把同域跨界做通，再谈异域）

提问举例「读到《聪明的投资者》→ 链接到价值投资策略」。核查 `PROFILE.md`：用户是智驾开发工程师，关注「端到端自动驾驶、BEV 感知、世界模型」+「量化涨停交易系统」。**这两个领域的真实交叉点比「读书 ↔ 价值投资」更具体**：

| 智驾技术 | 投研对应 | 交叉性质 |
|---|---|---|
| 时序模型（BEV 时序融合） | 情绪温度 Z 的时间序列（`market_sentiment` 的 ΔZ 速率） | **同构**：都是「状态 + 变化率」估计 |
| 世界模型 | 反事实推演（3.6） | **同构**：都是「给定干预预测后果」 |
| 端到端 vs 模块化 | 规则优先 + LLM 兜底（pipeline §1 决策） | **同构**：都是「可解释性与性能的权衡」 |
| 多传感器融合 + 冗余 | 6 层 z-score + 三维向量 + 三重护栏 | **同构**：都是「多源信号交叉确认 + 失效降级」 |
| corner case 处理 | 熔断机制 / 对抗性分析段 | **同构**：都是「显式建模尾部风险」 |

**落地路径**：

1. **不要建「读书笔记 ↔ 战法」这类弱关联**（容易变成提问自己担心的「什么都记但什么都不深」）。
2. **建「方法论同构」实体**，放 `10_Reference/` 的跨域层（或新建 `methodology/`）：
   ```markdown
   # methodology/multi-source-fusion.md
   type: methodology
   instances:
     - 智驾：多传感器融合（camera + lidar + radar）+ 冗余降级
     - 投研：6 层 z-score + 三维向量交叉确认 + 三重护栏
     - 知识图谱：四层关系推断（L1 精确 → L4 LLM 语义），逐层降置信度
   invariant: 多源独立信号交叉确认，单源失效不导致系统失效；置信度随推断层级递减
   ```
3. **判据（防稀释）**：一个方法论实体必须有 **≥ 2 个领域的具体实例 + 一条不变的 invariant**，否则不建。只有「读书感想 + 一个战法链接」不算方法论，那是普通双链，直接写在笔记里即可。

**优先级说明**：这一项**排在 4.1 之后**，因为同域跨界（情绪↔战法）有明确的日常消费场景（每天盘前），异域跨界（智驾↔投研）的消费场景是偶发的（写方案时才想到）。**先做高频的**。

### 4.3 【P2】元知识层：四构件本身是通用方法论

**价值**：★★★
**难度**：低
**依赖**：无

`ontology-knowledge-graph` skill 已蒸馏四构件方法论。核查发现：**这套方法论正在被投研子区使用，但没有被记录为可复用的元知识**。

落地：在 `10_Reference/index/MASTER_INDEX.md` 或新建 `methodology/ontology-4-components.md` 里，把四构件写成领域无关的模板，并标注「投研子区的实例化情况」：

| 构件 | 通用定义 | 投研实例化 | 当前状态 |
|---|---|---|---|
| 1 实体 | 有唯一标识的领域对象 | stocks/industries/strategies/... | ⚠️ 5/14 类有内容 |
| 2 关系 | 实体间的谓词连接 | 10 个谓词（MOC.md:38） | ⚠️ 平面，无 kind 维度（3.3） |
| 3 逻辑规则 | 可机器执行的约束/推断 | logic/ | ❌ 0 条（3.1 修复中） |
| 4 动作 | 状态流转与维护操作 | actions/ | ❌ 0 条（3.2 修复中） |

**价值**：这张表本身就是最好的「图谱健康度仪表盘」，且**下次给任何新领域建图谱时直接复用**（避免每次重新发明）。成本极低（一个文件），但把 skill 的方法论从「文档」变成「可核对的实例化清单」。

### 4.4 【纪律】防「什么都记但什么都不深」

**价值**：★★★★（作为约束）
**难度**：低

提问自己提出了这个担忧。给三条可执行判据（写进 `logic/cross-domain-gate.md`）：

1. **深度门槛**：跨域实体必须有 ≥ 2 个具体实例 + 1 条 invariant（见 4.2 第 3 点）。达不到 → 不建实体，用普通双链。
2. **消费门槛**：新建任何跨域实体前，回答「这个实体在哪个已有工作流里会被读到」。答不出 → 不建。**事实 2 的教训就是建了没人读**。
3. **单域优先**：跨域链接数 / 单域链接数 < 20%。超过说明在逃避本域的深挖。当前投研子区跨域链接 = 0，远未到这个风险，但 4.1、4.2 做完后要监控。

---

## 5. 人性化：贴合个人投研风格

### 5.1 【P1】交易日志实体 + 链接决策时点的图谱状态

**价值**：★★★★★
**难度**：中
**依赖**：1.1（报告已存档，是「当时图谱状态」的天然快照）

这是提问 6 个子方向里**唯一有独特价值且无法被其他工具替代**的一项。

**为什么价值高**：复盘的核心问题不是「这笔交易赚了还是亏了」，而是「**当时我看到的信号是什么，我的解读对不对**」。盘前报告已经把当时的信号存档了（`daily/` + `market_sentiment/daily/`），图谱已经把当时的战法/情绪映射存档了（4.1 之后）。**缺的只是「交易 → 当时状态」这条边**。

**落地路径**：

1. 新建 `trades/`（或放 `00_Active/`，因为交易是活跃项目而非参考资料——**PARA 语义上应在 00_Active**，建议 `00_Active/trades/`）。
2. `templates/trade.md`：
   ```yaml
   ---
   type: trade
   code: 003040
   name: 楚天龙
   side: buy
   date: 2026-09-05
   price: null            # 私有数据，见下方合规
   size_pct: null
   strategy: "first_plate"
   weather: "2026-09-05_pre_盘前情绪报告"
   sentiment_z: 0.1210
   divergence_d: 0.6593
   thesis: "首板 + 基因分达标，情绪中性偏修复，游资净买入"
   exit_plan: "止损-3% / 止盈+8% / 最大持有3日"
   outcome: null          # 平仓后填
   outcome_vs_plan: null  # 复盘填：是否按计划执行
   created: 2026-09-05
   ---
   ```
3. **复盘段**（平仓后填，这是价值所在）：
   ```markdown
   ## 复盘
   - 计划执行度：止损在 -3.2% 触发（计划 -3%，滑点可接受）
   - thesis 验证：「游资净买入」正确，但「首板次日溢价」未兑现
   - 图谱当时的信号：天气阴 + first_plate 适用 → 信号一致
   - 教训：背离度 D=0.66 偏高时，即使天气适用也应降仓位
   - → 反哺规则：sentiment-weather-mapping 需加 D>0.6 的降仓约束
   ```
4. **最后一步是关键**：复盘的教训**必须回流到 `logic/` 规则**。否则交易日志只是日记，不产生知识。这条回流机制本身写成 `logic/trade-feedback.md`（自动化规则）。

**合规约束（强制，不可协商）**：

`AGENTS.md` 工程底线 + `knowledge-graph-llm-pipeline.md` §8 明确「持仓/API key/`.vibe-research/` 内容绝不进 vault」，且 vault 是 GitHub 仓（`lzw9560/knowledge`，虽私有但仍是云端）。

- **价格、仓位金额、账户总值一律不写**，只写百分比（`size_pct`）或干脆不写。
- 或者：**`trades/` 不进 vault**，放本地 `.vibe-research/` 之外的私有目录，vault 里只存脱敏的复盘结论 + `logic/` 规则回流。
- `PROFILE.md` 已有先例：「密码/密钥/Token 一律不存此文件，如需记录只写 `[REDACTED]`」。交易数据应同等对待。

**建议在实施前明确选择哪种**——这是本项的唯一决策点，技术实现无难度。

### 5.2 【P2】个性化权重（短线 vs 价值）

**价值**：★★★
**难度**：中
**依赖**：5.1（无交易数据则权重无依据）

提问设想「短线重龙虎榜/情绪，价值重财务/估值」。核查 `PROFILE.md`：用户是「量化涨停交易系统」+ 关注打板情绪。**风格已经很明确是短线/打板**，不存在「需要图谱适配多种风格」的问题。

所以**不要做通用权重系统**（YAGNI），做一件事即可：

- 把 `PROFILE.md` 的「当前关注领域」+ 风格，写成 `logic/personal-weighting.md`：
  ```yaml
  type: logic
  rule_type: 推断规则
  style: 短线打板
  weight_high: [dragon-tiger, events, sentiment]   # 龙虎榜/事件/情绪 优先展示
  weight_low: [metrics, valuations]                # 财务/估值 次优先
  ```
- **消费方**：1.1 的报告模板按此权重排序「图谱关联」段；MOC.md 的导航顺序按此调整（把 `dragon-tiger/` `events/` 提到前面，`metrics/` `valuations/` 后置）。
- **连带决策**：这影响 3.4 的填充顺序。按权重，应该**先填 `dragon-tiger/` 和 `events/`，而不是先填 `valuations/`**。这与我在 3.4 建议的「先做 valuations（最易）」冲突——**难度排序 vs 价值排序的权衡**。建议：**按价值排序，先做 `dragon-tiger/`**，因为它是短线打板的核心数据且源仓有 `DragonTiger` + `Seat` + `BillboardDetail` 三个现成契约。`valuations/` 对短线风格价值低，可延后。

### 5.3 【P2】决策情绪标注（主观层）

**价值**：★★★
**难度**：低
**依赖**：5.1

提问设想「记我当时为什么买/卖」。这已被 5.1 的 `thesis` + 复盘段覆盖，**不需要独立机制**。

唯一补充：在 5.1 的 trade 模板里加一个 `emotion` 字段（`calm` / `fomo` / `panic` / `revenge`），复盘时统计「fomo 状态下的交易胜率 vs calm 状态」。

**这是可量化的自我认知**，且样本量天然累积。但注意 `AGENTS.md` 的样本量纪律：**n < 30 标「探索性」，不得作为定稿依据**。早期几十笔交易的情绪统计只能当线索，不能当结论。

### 5.4 【砍】偏好学习 / 相似实体推荐

**价值**：★★
**难度**：高
**建议**：**砍掉**

理由：

- 推荐系统需要行为埋点（记录用户查了哪些实体）。Obsidian 无原生埋点，要自建插件或解析 `.obsidian/workspace.json` 的历史，工程量大且脆弱。
- 图谱当前 70 个实体、5 类有内容（事实 3），**样本量根本不支持「推荐相似实体」**。推荐的前提是实体足够多、特征足够丰富。
- 用户是单人使用，风格明确（5.2）。单人 + 风格明确 = 推荐系统的价值趋近于 0（推荐解决的是「我不知道我该看什么」，而用户很清楚自己盯打板情绪）。
- 违反 YAGNI：这是把消费级产品特性套到个人工具上。

**替代**：1.1 的「图谱缺口」清单已经实现了「主动提示该看什么」，且是基于真实工作流而非行为猜测。够用。

---

## 6. 开放性：对接外部知识源

### 6.1 【P1】newsradar：先扩 A股源，再谈抽取

**价值**：★★★
**难度**：中
**依赖**：无（但**顺序不可颠倒**）

提问设想「接研报/新闻 RSS → 自动抽取进 inbox（newsradar 已有 108 源）」。核查 `backend/news_sources.json`：

```
sources: 108
industries: 12（ai/semi/robot/auto/energy/bio/space/security/tech/consumer/macro/science）
A股/财经源: 3（华尔街见闻、东方财富股票、东方财富资讯）
其余样本: OpenAI, Google Research, Hugging Face, 量子位, MIT Tech Review AI
```

**结论：当前 newsradar 是科技资讯雷达，不是投研资讯雷达。** 12 个 industries 是科技产业分类，与图谱的 `industries/`（白酒/电池/黄金/半导体/汽车整车/通信设备/半导体封测，证监会+概念分类）**口径完全不同**。

直接接抽取会发生什么：108 源产出的是「OpenAI 发布 GPT-6」这类新闻，抽出的实体是 AI 公司/技术概念，与 A股图谱无法对齐 → inbox 被科技新闻淹没 → 质量门失守 → 违反「不直接灌入是知识图谱健康的第一道防线」（`inbox/index.md:4`）。

**落地路径（严格分两步）**：

1. **第一步：扩源（不做抽取）**。往 `news_sources.json` 加 A股投研源，并**新增一个 industry key `astock`**（不复用现有 12 个科技分类，避免口径混淆——这正是 `AGENTS.md`「跨数据源的比较必须先验证数据口径一致性」的要求）：
   - 已有可复用：源仓已接 `eastmoney-searchapi` / `cninfo`（巨潮公告）/ `rss-newsradar` 三个数据源实体，其中 cninfo 是**公告权威源**，优先级最高。
   - 建议新增：财联社电报、交易所公告（沪深）、券商研报 RSS。
   - **`trading-agents` 项目已接财联社**（见 `multi-project-integration-plan.md` 附录 A.1），可复用其接入代码。
2. **第二步：抽取（只在 `astock` 分类内）**。按 pipeline §3 的 **P2 研报抽取 prompt**（已设计好，约束完整：实体类型限定 stock/industry/concept/analyst/metric/event，关系限定 belongs_to/tagged/covered_by/has_metric/authored_by，股票优先用 6 位代码，全部标 source）。输出进 `inbox/`，走 1.3 的晋级流程。

**纪律**：第二步启动前，第一步的 A股源必须 ≥ 20 个且稳定运行 2 周。**不要边扩源边抽取**——那会让 inbox 里混入科技新闻噪声，事后清理成本远高于等待成本。

### 6.2 【P2】trading-agents 辩论结果 → insight 实体

**价值**：★★★★
**难度**：中
**依赖**：3.3（causal 边规范）、6.1 第二步（抽取通道）

`trading-agents` 有 7 个 AI Analyst（市场/舆情/新闻/基本面/政策/游资/解禁）+ Bull/Bear 辩论 + 三方风险辩论（`multi-project-integration-plan.md` 附录 A.1 已探查确认）。

**这是 vault 里没有的实体类型**：辩论结论既不是事实（不能进 `events/`），也不是规则（不能进 `logic/`），是**带论证过程的判断**。

**落地路径**：

1. 新建 `insights/`（`type: insight`），模板：
   ```yaml
   ---
   type: insight
   code: 003040
   date: 2026-09-05
   source_project: trading-agents
   bull_case: "..."
   bear_case: "..."
   verdict: "..."
   risk_debate: "..."
   confidence: medium          # AI 产出 → 上限 medium，不给 high（pipeline §4）
   inferred_by: llm            # 必须标（pipeline §4：L4 LLM 语义 → confidence: low + inferred_by）
   exploratory: true
   ---
   ```
2. **强制进 inbox**（pipeline §4：LLM 产出必须过质量门）。辩论结果是 LLM 产出，**不能直接进正式区**。
3. **与 5.1 的交易日志对接**：`trade.md` 的 `thesis` 可以引用 `2026-09-05-003040`，复盘时对比「AI 辩论结论 vs 我的判断 vs 实际结果」。这是三方交叉验证，价值高。
4. **纪律**：`AGENTS.md` 明确 AI 产出「样本量 <30 标探索性，不得作为定稿依据」。所以 insight 实体**不能作为 `causal` 边的 evidence**（3.3），只能作为线索。这条写进 `logic/`。

**时机**：建议在 `trading-agents` 纳入图谱时一并做（`multi-project-integration-plan.md` §6.1 已定 trading-agents 为第一优先纳入项目）。**但见 6.4 的暂缓建议。**

### 6.3 【暂缓】a-Plate-Sentinel 情绪数据

**价值**：★★★（潜在）
**难度**：高
**建议**：**维持已有决策，暂缓**

`multi-project-integration-plan.md` §0.3 事实 3 + R4 已明确：a-Plate-Sentinel 处于 MVP 骨架阶段（README 自述「数据模型+计算服务骨架已生成，待补全算法细节与 API/前端」，AGENTS.md 明确龙虎榜席位引擎/回测/AI 复盘 Agent 留 Phase 2），纳入会产生大量「待补」占位实体，违背 inbox 质量门原则。

**这个决策是正确的，保持。** 触发条件已在 R4 定义（情绪看板实现 + 闭环验证通过）。

**补充一点**：提问设想「接 a-Plate-Sentinel 的情绪数据 → 存为情绪时间线」。但 `market_sentiment/` 子区**已经在做情绪时间线**（6 层 z-score、三维向量、daily/ 报告）。两者会重叠。等 a-Plate-Sentinel 的 STI（情绪温度指数，7 维加权）实现后，**第一件事应该是判断它与 `market_sentiment` 的 composite_z 是否同一口径**——如果是，选一个；如果不是，明确各自适用范围。不要两套情绪指数并行。

### 6.4 【暂缓】多项目纳入（已有 718 行方案，但时机不对）

**价值**：★★★
**难度**：高
**建议**：**暂缓，先打通单项目闭环**

`docs/multi-project-integration-plan.md`（718 行，状态「设计草案待评审」）已经把多项目纳入设计得很完整：方案 D（项目实体 + 双字段 `project`/`projects` + 平铺不分子文件夹 + 新建 `agents/` 分流 AI 角色与真人分析师），4 个方案对比 + 三段式决策 + 8 项风险 + 探查附录。**这份设计本身质量高，方案 D 的论证（尤其「共享实体是图谱主体价值，子文件夹会割裂跨项目连接」）是正确的。**

**但建议暂缓执行，理由是时机而非设计**：

1. **该方案自己的 R7 未决项写「indices/reports/metrics/valuations/dragon-tiger/events 实体数未探查」**。本次核查给出答案：**全部为 0**（事实 3）。所以 §3.3 的「存量迁移 54+ 实体加字段」实际是 70 个实体，且其中 9 个目录是空壳——迁移范围比设计假设的大，而迁移的价值比设计假设的小（给空目录的 index.md 加 `projects:` 字段毫无意义）。
2. **单项目闭环尚未打通**：事实 2（0 双链）+ 事实 4（审查闭环假）+ 事实 1（零重叠）。在这个状态下纳入第 2、3 个项目，结果是**三个项目都零消费**。横向扩张不解决纵向失效。
3. **类比**：这相当于「单个服务还没有一个真实用户，就开始做微服务拆分」。

**建议的顺序**：

```
现在：Vibe-Research 单项目 + market_sentiment 互链（4.1）+ 报告消费（1.1）
      ↓ 验证：连续 2 周报告有图谱双链、审查工单有关闭记录、stocks 与热点重叠率 > 30%
然后：纳入 trading-agents（按已有方案 D，设计可直接用）
      ↓ 验证：insights 实体被 trade 复盘引用 ≥ 5 次
再后：daily-stock-analysis（战法 origin 问题，R2）
最后：a-Plate-Sentinel（R4 触发条件满足后）
```

**方案 D 的设计文档保持不动**，它是对的，只是排队靠后。唯一需要更新的是 R7（实体数已探查清楚：全 0）和 §3.3（迁移表按实际 70 个实体 + 9 个空目录重写）。

### 6.5 【P1】MCP 生态：让外部 agent 读写图谱

**价值**：★★★★
**难度**：中
**依赖**：1.4（MCP 配起来）

见 1.4。补充「外部 agent 写」的纪律：

- **写必须过 inbox**。外部 agent（trading-agents 的 7 Analyst、daily-stock-analysis 的 Agent 策略问股）通过 MCP 的 `create_note` 写入时，路径必须落在 `inbox/`，不能直接写正式区。这条写进 `logic/`（3.1）并由 MCP 侧的路径约束实现。
- **`move_note` 是危险操作**（会重写全库反向链接），只对人工开放，agent 不可调用。
- pipeline §7 的 8 个工具里，`get_vault_guide()` 应该是 agent 的**第一个调用**（先学规范再写），这个设计是对的，保持。

---

## 7. 建议砍掉或暂缓（YAGNI）

明确列出不该做的事，与该做的事同等重要。当前图谱的问题不是功能不够，是**已有功能没被用起来**（事实 2、4）。

| 项 | 来源 | 处置 | 理由 |
|---|---|---|---|
| 前端「图谱关联节点数」徽标 | 提问 1 | **砍**（改为 Obsidian URI 外链） | 跨系统耦合成本高；当前节点数暴露贫瘠反而降低打开意愿；消费场景错配。替代方案成本近零（见 1.5） |
| 反事实推理 | 提问 3 | **暂缓**（设前置条件） | causal 边实例数 = 0，事件实体 = 0。在空图上做传播输出噪声，且会被误信为洞察，违反「不臆造数据」 |
| 偏好学习 / 相似实体推荐 | 提问 5 | **砍** | 需行为埋点（Obsidian 无原生支持）；70 实体不支持推荐；单人 + 风格明确 = 推荐价值趋近 0。1.1 的缺口清单已覆盖「主动提示该看什么」 |
| 社区发现（Louvain） | 提问 3 | **暂缓** | 节点稀疏 + 真实边少（入边 Top 是 index 文件），会退化成单点集合。等实体 > 200 且边密度达标 |
| a-Plate-Sentinel 纳入 | 提问 6 | **暂缓**（维持已有 R4 决策） | MVP 骨架阶段，纳入产生占位实体，违背 inbox 质量门 |
| 多项目纳入（trading-agents / daily-stock-analysis） | 提问 6 | **暂缓**（设计方案保留，排队靠后） | 单项目闭环未打通（0 双链 + 假闭环 + 零重叠）。横向扩张不解决纵向失效 |
| 置信度时间衰减算法 | 提问 2 | **砍**（改为 `last_verified` 日期） | 衰减速率无数据支撑（违反 `AGENTS.md`「参数选择必须有数据支撑」）；且会让 confidence 承载「抽取可靠度」+「新鲜度」两个正交语义 |
| 通用个性化权重系统 | 提问 5 | **砍**（改为单条 `logic/personal-weighting.md`） | 用户风格已明确是短线打板，不存在多风格适配需求 |
| `metrics/` 财务数据全量导入 | 提问 3 | **暂缓** | 短线风格下价值低（5.2 权重）；口径复杂（`AGENTS.md` 要求先验证跨源口径一致性）。先做 `dragon-tiger/` + `events/` |
| 跨域「读书笔记 ↔ 战法」弱关联 | 提问 4 | **砍** | 提问自己担心的「什么都记但什么都不深」正是这类。改为「方法论同构」实体 + 深度门槛（4.2、4.4） |
| newsradar 直接接抽取 | 提问 6 | **暂缓抽取，先扩源** | 108 源中仅 3 个 A股财经源，其余是 AI 科技资讯。直接抽取会用科技新闻淹没 inbox |

---

## 8. 优先级矩阵

**评分口径**：
- **影响** = 对「图谱被真实消费」的贡献（不是对「图谱变大」的贡献）
- **难度** = 实施成本（低 < 1 天 / 中 1-3 天 / 高 > 3 天）
- **依赖** = 必须先完成的前置项

### P0：立即做（本周内，全部低难度或已有基础）

| # | 项 | 影响 | 难度 | 依赖 | 修复的事实 |
|---|---|---|---|---|---|
| 1.1 | 盘前/盘后报告注入图谱关联段 | ★★★★★ | 低 | — | 事实 2（0 双链）、事实 1（提供缺口清单） |
| 1.2 | 修 `matched_strategies` 死查询 | ★★★★★ | 低 | — | 战法↔股票双向边缺失 |
| 2.2 | 修审查脚本（36 误报 + 断链分级 + hub 排除 index） | ★★★★★ | 低 | — | 事实 4（high 101 → ~10） |
| 2.1 | 审查报告 → `.scratch/` 工单 + 「本期关闭」段 | ★★★★★ | 低 | 2.2 | 事实 4（假闭环） |
| 4.1 | `market_sentiment` ↔ `investing` 互链（情绪天气↔战法映射） | ★★★★★ | 低 | — | 两孤岛 + 12 战法「适用天气」不可执行 |
| 3.1 | `logic/` 填充 6 条实证规则 | ★★★★★ | 中 | — | 事实 3（四构件缺 2） |

**P0 的共同特征**：全部不需要新数据源、不需要新插件、不需要外部项目。**只是把已存在的东西连起来 + 修已有的 bug**。这是「乘数最小项」的修复。

### P1：次批（2-4 周）

| # | 项 | 影响 | 难度 | 依赖 |
|---|---|---|---|---|
| 1.3 | 热点股 30 秒入图通道（inbox stub） | ★★★★★ | 中 | 1.1 |
| 3.2 | `actions/` 填充 | ★★★ | 低 | 3.1 |
| 2.3 | 战法卡去副本化 + 漂移检测 | ★★★★ | 中 | 2.2 |
| 2.4 | `.entity-dictionary.json` 落地 | ★★★★ | 中 | 2.2 |
| 1.4 | MCP 配置 + 3 个高频查询验证 | ★★★★ | 中 | 1.2 |
| 5.1 | 交易日志实体 + 复盘回流 `logic/` | ★★★★★ | 中 | 1.1（**+ 合规决策**） |
| 3.3 | 关系谓词加 `kind`（causal/correlational/structural） | ★★★★ | 中 | 3.1 |
| 6.5 | MCP 写入纪律（agent 只能写 inbox） | ★★★★ | 中 | 1.4 |
| 6.1 第一步 | newsradar 扩 A股源（新增 `astock` industry） | ★★★ | 中 | — |

### P2：第三批（1-2 月，需前置数据积累）

| # | 项 | 影响 | 难度 | 依赖 |
|---|---|---|---|---|
| 3.4 | `dragon-tiger/` + `events/` 填充（按 5.2 权重，先龙虎榜后估值） | ★★★★★ | 高 | 1.3、2.5 |
| 2.5 | `last_verified` / `data_asof` + frontmatter 去时点数据 | ★★★ | 中 | 3.4 |
| 3.5 | 度中心性 + 最短路径（networkx，结果写回 reviews/） | ★★★ | 中 | 3.4 |
| 5.2 | `logic/personal-weighting.md`（单条，非系统） | ★★★ | 低 | 5.1 |
| 5.3 | trade 的 `emotion` 字段 + 情绪胜率统计 | ★★★ | 低 | 5.1 |
| 4.2 | 方法论同构实体（智驾 ↔ 投研） | ★★★ | 中 | 4.1 |
| 4.3 | 元知识层（四构件实例化清单） | ★★★ | 低 | 3.1、3.2 |
| 4.4 | 跨域深度门槛三条判据 | ★★★★ | 低 | — |
| 6.1 第二步 | newsradar 抽取（用 pipeline P2 prompt） | ★★★ | 中 | 6.1 第一步稳定 2 周 |
| 6.2 | `insights/` 实体（trading-agents 辩论） | ★★★★ | 中 | 3.3、6.4 |

### 暂缓 / 砍

见第 7 节（11 项）。

### 矩阵视图（影响 × 难度）

```
影响 ★★★★★ ┃  1.1  1.2  2.2  2.1  4.1        │  1.3  5.1  3.1
           ┃  （P0 低难度——全部先做）        │  （P1 中难度）
           ┃                                  │
影响 ★★★★  ┃  4.4                            │  2.3  2.4  1.4  3.3  6.5  6.2
           ┃                                  │
影响 ★★★   ┃  3.2  5.2  5.3  4.3             │  2.5  3.5  4.2  6.1
           ┃                                  │
影响 ★★    ┃                                  │  3.4（高难度但影响★★★★★，
           ┃                                  │   因依赖多故排 P2）
           ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━
              难度：低                          难度：中 / 高

   砍掉区（不进任何批次）：前端徽标、反事实推理、偏好学习推荐、
                          置信度衰减、通用权重系统、Louvain、
                          读书笔记弱关联、metrics 全量导入
```

**读法**：左上角 5 项（1.1 / 1.2 / 2.2 / 2.1 / 4.1）是**全案的核心**——影响 ★★★★★ 且难度低且无依赖。这 5 项做完，图谱就从「0 双链的孤岛」变成「每天被两份报告消费的活库」。其余所有项都是在这 5 项基础上的延伸。

---

## 9. 30 天落地路线

### Week 1：连接与降噪（P0 低难度 5 项）

| 天 | 动作 | 产出 | 验收 |
|---|---|---|---|
| D1 | 2.2 修 `vault_audit.py`：`schema_infer` 读正文 + 断链三级分流 + `relation_density` 排除 index | 脚本 commit | 重跑审查：high 从 101 → < 15 |
| D2 | 4.1 建 `logic/sentiment-weather-mapping.md`（**先查 S031/S047 回测结论，有数据填数据，无数据标 `exploratory: true`**） | 1 个 logic 实体 | 12 张战法卡的「适用天气」段改为链接此规则 |
| D3 | 1.1 改盘前报告生成器：注入「📚 图谱关联」段 + 命中双链 + 缺口待办 | 报告模板 commit | 生成的报告双链数 > 0 |
| D4 | 1.2 脚本提取 `stocks/*.md` 正文的 `strategies/` → frontmatter `matched_strategies` | 11 个实体更新 | `strategies/dragon_head.md` 的「匹配股票」表非空 |
| D5 | 2.1 `vault_audit.py` 输出 `.scratch/kg-audit/` 工单 + 报告加「本期关闭」段 | 脚本 + 工单目录 | 周日 CI 报告含工单链接 |
| D7 | 跑周日 CI，人工关闭工单 | 第 2 份审查报告 | `findings_count` 环比下降，「本期关闭」非空 |

**Week 1 结束时的状态**：事实 2（0 双链）和事实 4（假闭环 + 误报）已修复。图谱第一次被日常工作流消费。

### Week 2：构件补全与入图通道（P0 剩余 + P1 启动）

| 天 | 动作 | 产出 |
|---|---|---|
| D8-9 | 3.1 填充 `logic/` 6 条实证规则（inbox-promotion / stub-trigger / schema-body-fallback / broken-link-grading / source-drift / static-value-ban），**每条必须在 `vault_audit.py` 有对应检查函数** | 6 个 logic 实体 + 脚本 |
| D10 | 3.2 填充 `actions/` 3 条（promote-from-inbox / weekly-audit / sync-from-source） | 3 个 action 实体 |
| D11-12 | 1.3 热点股入图通道：QuickAdd 命令 + `astock.py:individual_info()` 取字段 + inbox stub 模板 + 晋级规则 | 入图通道可用 |
| D13 | 用 Week 1 累积的「图谱缺口」清单，批量建档（**只建被 ≥2 份报告命中的**） | inbox 若干 stub |
| D14 | 周日 CI + 首次 inbox 晋级（mv 到 `stocks/`） | `stocks/` 实体增长 |

**Week 2 结束时**：四构件 4/4（事实 3 修复），`stocks/` 开始包含真实热点股（事实 1 开始修复）。

### Week 3-4：去副本化 + MCP + 交易日志（P1 主体）

| 动作 | 产出 |
|---|---|
| 2.3 战法卡去副本化：删正文拷贝、加 `source_sha`、结构化条件进 frontmatter；审查脚本加第 9 项漂移检测 | 12 张战法卡瘦身 + 漂移检测 |
| 2.4 `.entity-dictionary.json` 落地：扫 vault + 源仓 60 spec + `astock.py` 股票列表，标 `not_imported` | 词典文件 + 断链分级消费方 |
| 1.4 MCP 配置：按 `docs/obsidian-mcp-setup.md` 装 `yanxue06/obsidian-mcp`，验证 3 个查询；`AGENTS.md` 会话协议加「先 `query_dataview` 再回答」 | MCP 可用 |
| 5.1 **先做合规决策**（价格/仓位写不写 vault），再建 `00_Active/trades/` + 模板 + 复盘回流规则 | 交易日志机制 |
| 3.3 关系谓词加 `kind` 维度 + `causal` 边的 evidence/sample_size 强制约束 | 关系分类法 |
| 6.1 第一步 newsradar 扩 A股源（新增 `astock` industry key，复用 `trading-agents` 的财联社接入） | ≥ 20 个 A股源 |

### Week 4 末：验证与决策点

**验证指标**（全部可量化）：

| 指标 | Week 0 基线 | Week 4 目标 |
|---|---|---|
| `daily/` + `market_sentiment/daily/` 报告的双链数 | **0** | ≥ 10/份 |
| 审查报告 high 级发现数 | **101**（含 36 误报） | < 15（真实问题） |
| 审查跟踪清单关闭率 | **0%**（4/4 复选框空） | > 60% |
| 四构件填充度 | **2/4** | 4/4 |
| 空壳实体目录数 | **9** | ≤ 6（`dragon-tiger/` 优先填） |
| `stocks/` 与盘前报告 Top 榜重叠率 | **0%** | > 30% |
| `.entity-dictionary.json` | **不存在** | 存在且覆盖源仓 60 spec |
| MCP 可用 | **否** | 是（3 个查询验证通过） |
| 战法卡副本漂移风险 | **12/12 暴露** | 0（去副本化 + 检测） |

**Week 4 决策点**：以上指标达标 → 启动 6.4（纳入 `trading-agents`，`multi-project-integration-plan.md` 方案 D 可直接用，只需先更新其 R7 和 §3.3）。未达标 → **继续打磨单项目闭环，不扩张**。

---

## 附：与已有设计文档的关系（不另起炉灶）

本文档是**诊断 + 优先级重排**，不替代已有设计。三份已有文档的处置：

| 文档 | 状态 | 本文档的处置 |
|---|---|---|
| `docs/knowledge-graph-llm-pipeline.md` | 设计完整，实现缺位（词典未建、MCP 未配、P1-P5 未跑） | **设计全部保留**。本文档只是把它的 §2（词典）排到 P1、§5（stub）复用到 1.3、§7（MCP）排到 P1。不修改任何设计决策 |
| `docs/multi-project-integration-plan.md`（718 行） | 设计草案待评审，方案 D 论证正确 | **设计保留，执行暂缓**（6.4）。需更新两处：R7（实体数已探查：`indices/reports/metrics/valuations/dragon-tiger/events` 全为 0）、§3.3（迁移表按实际 70 实体 + 9 空目录重写） |
| `ontology-knowledge-graph` skill | 四构件方法论 | **完全对齐**。本文档的 3.1/3.2 就是把方法论的构件 3、4 从「已蒸馏」变成「已实例化」；4.3 建议把方法论本身记录为元知识 |

**唯一的路线变更**：提问假设的顺序是「消费层 → 活起来 → 深度 → 跨界 → 人性化 → 开放性」，本文档基于实证重排为「**连接与降噪（P0 六项）→ 构件补全 → 去副本化与工具化 → 数据填充 → 横向扩张**」。变更依据是第 0 节的五个硬事实。

---

**Version:** 1.0.0
**性质**：建议稿，待评审。所有数字基于 2026-09-06 实际核查，可用文中给出的命令复现。
