#!/usr/bin/env python3
"""批量更新所有实体类型的格式——应用 callout+emoji+Dataview 样式。

与 update_stock_format.py 互补：本脚本处理 stocks 之外的所有实体类型。

各实体类型的转换规则：
  industries/concepts → 加 callout + emoji + 成分股 Dataview(全路径) + 关联段
  data-sources        → 加 callout(📡) + 提供字段 + 限流 + 降级 + 关联实体
  specs               → 加 callout(📋) + 问题/需求/验收/关联
  agents              → 加 callout(🤖) + 职责 + 辩论对手 + 数据源
  dragon-tiger        → 加 callout(🐉) + 席位 + 游资画像
  events              → 加 callout(⚡) + 影响标的 + 连板梯队
  metrics             → 加 callout(💰) + 财务摘要 + 趋势
  valuations          → 加 callout(📈) + 估值指标 + 历史分位
  reports             → 加 callout(📰) + 报告摘要 + 分析师
  analysts            → 加 callout(👤) + 覆盖领域 + 近期研报
  indices             → 加 callout(📊) + 成分股
  logic               → 加 callout(⚙️) + 规则定义 + 执行逻辑
  actions             → 加 callout(⚡) + 动作定义 + 执行步骤

策略：
  - frontmatter 保持不变
  - 在 frontmatter 后插入 callout 信息卡
  - 各段标题加 emoji
  - Dataview 查询统一用全路径 FROM + WITHOUT ID + LIMIT
  - 末尾加关联段（出链/入链计数）
  - 已有正文内容尽量保留（提取后重新插入对应段）

用法:
    python3 scripts/update_all_formats.py            # 全量更新
    python3 scripts/update_all_formats.py --dry-run  # 只预览不写盘
    python3 scripts/update_all_formats.py industries # 仅更新指定类型
"""
import argparse
import re
import sys
from pathlib import Path

VAULT = Path("/Users/lizhiwei/Documents/Obsidian Vault/10_Reference/investing")

# 各实体类型配置：(文件夹名, frontmatter type 值, emoji, callout标题, 是否处理)
ENTITY_TYPES = {
    "industries":    ("industry",      "🏭", "行业信息"),
    "concepts":      ("concept",       "💡", "概念信息"),
    "data-sources":  ("data_source",   "📡", "数据源"),
    "specs":         ("spec",          "📋", "项目决策"),
    "agents":        ("agent_role",    "🤖", "AI 角色"),
    "dragon-tiger":  ("dragon_tiger",  "🐉", "龙虎榜"),
    "events":        ("event",         "⚡", "事件"),
    "metrics":       ("metric",        "💰", "财务指标"),
    "valuations":    ("valuation",     "📈", "估值快照"),
    "reports":       ("report",        "📰", "研报"),
    "analysts":      ("analyst",       "👤", "分析师"),
    "indices":       ("index",         "📊", "指数"),
    "logic":         ("logic",         "⚙️", "规则"),
    "actions":       ("action",        "⚡", "动作"),
}


def parse_file(filepath: Path) -> tuple[str | None, str]:
    """分离 frontmatter 与正文。返回 (fm_text, body)。"""
    content = filepath.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)\Z", content, re.DOTALL)
    if not m:
        return None, content
    return m.group(1), m.group(2)


def get_fm_field(fm: str, key: str) -> str:
    """提取 frontmatter 标量字段值。"""
    m = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", fm, re.MULTILINE)
    if not m:
        return ""
    v = m.group(1).strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v


def extract_body_sections(body: str) -> dict[str, str]:
    """提取正文中的各段内容。返回 {段名: 内容}。"""
    sections = {}
    # 匹配 # 或 ## 标题段
    pattern = r"^#{1,2}\s+(.+?)\s*\n(.*?)(?=\n#{1,2}\s|\Z)"
    for m in re.finditer(pattern, body, re.DOTALL | re.MULTILINE):
        title = m.group(1).strip()
        content = m.group(2).strip()
        # 去掉 emoji 前缀
        title = re.sub(r"^[^\u4e00-\u9fff\w]+\s*", "", title)
        sections[title] = content
    return sections


def build_callout(fm: str, entity_type: str, emoji: str, callout_title: str) -> str:
    """构建 [!info] callout 信息卡。"""
    configs = {
        "industry": lambda: f"""> [!info] {emoji} {callout_title}
> **行业**：{get_fm_field(fm, 'name')}  **来源**：{get_fm_field(fm, 'source')}
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[concepts/]] · [[data-sources/]]""",
        "concept": lambda: f"""> [!info] {emoji} {callout_title}
> **概念**：{get_fm_field(fm, 'name')}  **关联行业**：{get_fm_field(fm, 'related_industry')}
> **成分股数**：`=(length(filter(this.file.inlinks, (l) => l.folder = "stocks")))`
>
> **关联**：[[industries/]] · [[data-sources/]]""",
        "data_source": lambda: f"""> [!info] {emoji} {callout_title}
> **名称**：{get_fm_field(fm, 'name')}  **层级**：L{get_fm_field(fm, 'layer')}
> **接口**：`{get_fm_field(fm, 'endpoint')}`
> **限流**：`{get_fm_field(fm, 'rate_limit')}`  **降级**：`{get_fm_field(fm, 'fallback')}`""",
        "spec": lambda: f"""> [!info] {emoji} {callout_title}
> **编号**：{get_fm_field(fm, 'number')}  **标题**：{get_fm_field(fm, 'title')}  **状态**：{get_fm_field(fm, 'status')}
>
> **关联**：[[specs/]] · [[strategies/]] · [[data-sources/]]""",
        "decision": lambda: f"""> [!info] {emoji} {callout_title}
> **编号**：{get_fm_field(fm, 'number')}  **标题**：{get_fm_field(fm, 'title')}  **状态**：{get_fm_field(fm, 'status')}
>
> **关联**：[[specs/]] · [[data-sources/]]""",
        "project": lambda: f"""> [!info] {emoji} {callout_title}
> **名称**：{get_fm_field(fm, 'name')}  **标题**：{get_fm_field(fm, 'title')}  **状态**：{get_fm_field(fm, 'status')}
> **GitHub**：`{get_fm_field(fm, 'github')}`
>
> **关联**：[[specs/]] · [[data-sources/]] · [[agents/]]""",
        "agent_role": lambda: f"""> [!info] {emoji} {callout_title}
> **角色**：{get_fm_field(fm, 'name')}  **职能**：`{get_fm_field(fm, 'role')}`
> **来源项目**：{get_fm_field(fm, 'origin_project')}
> **辩论对手**：{get_fm_field(fm, 'debates_with')}""",
        "dragon_tiger": lambda: f"""> [!info] {emoji} {callout_title}
> **股票**：`{get_fm_field(fm, 'code')}`  **日期**：{get_fm_field(fm, 'date')}
> **机构净额**：{get_fm_field(fm, 'institution_net')}  **席位**：{get_fm_field(fm, 'seats')}
>
> **关联**：[[stocks/]] · [[events/]]""",
        "event": lambda: f"""> [!info] {emoji} {callout_title}
> **日期**：{get_fm_field(fm, 'date')}  **类型**：{get_fm_field(fm, 'event_type')}
> **来源**：{get_fm_field(fm, 'source')}
> **摘要**：{get_fm_field(fm, 'summary')}""",
        "metric": lambda: f"""> [!info] {emoji} {callout_title}
> **股票**：`{get_fm_field(fm, 'code')}`  **报告期**：{get_fm_field(fm, 'period')}
> **营收**：{get_fm_field(fm, 'revenue')}  **净利**：{get_fm_field(fm, 'net_profit')}  **EPS**：{get_fm_field(fm, 'eps')}
>
> **所属股票**：[[stocks/]]""",
        "valuation": lambda: f"""> [!info] {emoji} {callout_title}
> **股票**：`{get_fm_field(fm, 'code')}`  **PE(TTM)**：{get_fm_field(fm, 'pe_ttm')}  **PB**：{get_fm_field(fm, 'pb')}
> **PE 分位**：{get_fm_field(fm, 'pe_percentile')}%  **PB 分位**：{get_fm_field(fm, 'pb_percentile')}%
>
> **所属股票**：[[stocks/]]""",
        "report": lambda: f"""> [!info] {emoji} {callout_title}
> **标题**：{get_fm_field(fm, 'title')}  **机构**：{get_fm_field(fm, 'org')}
> **日期**：{get_fm_field(fm, 'publish_date')}  **评级**：{get_fm_field(fm, 'report_type')}
> **分析师**：{get_fm_field(fm, 'researcher')}
>
> **覆盖标的**：[[stocks/]]""",
        "analyst": lambda: f"""> [!info] {emoji} {callout_title}
> **姓名**：{get_fm_field(fm, 'name')}  **机构**：{get_fm_field(fm, 'org')}
> **覆盖数**：{get_fm_field(fm, 'coverage_count')}
>
> **关联**：[[reports/]] · [[stocks/]]""",
        "index": lambda: f"""> [!info] {emoji} {callout_title}
> **代码**：`{get_fm_field(fm, 'code')}`  **名称**：{get_fm_field(fm, 'name')}  **市场**：{get_fm_field(fm, 'market')}
>
> **关联**：[[stocks/]] · [[data-sources/]]""",
        "logic": lambda: f"""> [!info] {emoji} {callout_title}
> **规则**：`{get_fm_field(fm, 'rule_id')}`  **类型**：{get_fm_field(fm, 'rule_type')}
> **严重级**：{get_fm_field(fm, 'severity')}  **适用实体**：{get_fm_field(fm, 'target_entity')}
>
> **违反处置**：`{get_fm_field(fm, 'action_on_violation')}`""",
        "action": lambda: f"""> [!info] {emoji} {callout_title}
> **动作**：`{get_fm_field(fm, 'action_id')}`  **类型**：{get_fm_field(fm, 'action_type')}
> **触发**：`{get_fm_field(fm, 'trigger')}`  **目标**：`{get_fm_field(fm, 'target')}`
>
> **触发自**：[[logic/]]""",
    }
    builder = configs.get(entity_type)
    if builder:
        return builder()
    return f"> [!info] {emoji} {callout_title}"


def get_section_content(sections: dict, names: list[str], default: str = "") -> str:
    """从提取的段中查找内容，按优先级匹配多个可能名称。"""
    for name in names:
        for key, content in sections.items():
            if name in key:
                return content
    return default


def build_relation_footer() -> str:
    """构建通用的关联段尾注。"""
    return """## 🔗 关联

- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个"""


def build_industry_body(fm: str, sections: dict) -> str:
    code = get_fm_field(fm, "code")
    name = get_fm_field(fm, "name")
    overview = get_section_content(sections, ["行业概览", "概览"], "")
    members_intro = get_section_content(sections, ["成分股", "下属"], "")

    parts = []
    if overview:
        parts.append(f"## 📊 行业概览\n\n{overview}\n")
    else:
        parts.append("## 📊 行业概览\n\n待补充\n")

    parts.append("""## 🏢 成分股

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  pe_ttm AS "PE",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND industry = this.name
SORT market_cap DESC
LIMIT 20
```""")

    parts.append("""## 💰 资金流向

- 数据源：[[data-sources/eastmoney-push2|东财 push2]]""")

    parts.append("""## 📰 行业研报

```dataview
TABLE WITHOUT ID
  publish_date AS "日期",
  org AS "机构",
  researcher AS "分析师",
  title AS "标题"
FROM "10_Reference/investing/reports"
WHERE type = "report" AND contains(code, this.code)
SORT publish_date DESC
LIMIT 10
```""")

    parts.append("""## ⚡ 近期事件

```dataview
TABLE WITHOUT ID
  date AS "日期",
  event_type AS "类型",
  summary AS "摘要"
FROM "10_Reference/investing/events"
WHERE type = "event" AND contains(codes, this.code)
SORT date DESC
LIMIT 10
```""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_concept_body(fm: str, sections: dict) -> str:
    overview = get_section_content(sections, ["概念概览", "概览"], "")
    rotation = get_section_content(sections, ["题材轮动", "轮动"], "")

    parts = []
    if overview:
        parts.append(f"## 📊 概念概览\n\n{overview}\n")
    else:
        parts.append("## 📊 概念概览\n\n待补充\n")

    parts.append("""## 🏢 成分股

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND contains(concept, this.name)
SORT market_cap DESC
LIMIT 20
```""")

    if rotation:
        parts.append(f"## 🔄 题材轮动\n\n{rotation}\n")
    else:
        parts.append("""## 🔄 题材轮动

- **发酵期**：
- **高潮期**：
- **退潮期**：""")

    parts.append("""## 💰 资金流向

- 数据源：[[data-sources/eastmoney-push2|东财 push2]]""")

    parts.append("""## 📰 相关研报

```dataview
TABLE WITHOUT ID
  title AS "标题",
  org AS "机构",
  publish_date AS "日期"
FROM "10_Reference/investing/reports"
WHERE type = "report" AND contains(code, this.code)
SORT publish_date DESC
LIMIT 10
```""")

    parts.append("""## ⚡ 近期事件

```dataview
TABLE WITHOUT ID
  date AS "日期",
  event_type AS "类型",
  summary AS "摘要"
FROM "10_Reference/investing/events"
WHERE type = "event" AND contains(codes, this.code)
SORT date DESC
LIMIT 10
```""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_data_source_body(fm: str, sections: dict) -> str:
    fields = get_section_content(sections, ["提供字段", "字段"], "")
    rate_limit = get_section_content(sections, ["限流策略", "限流"], "")
    fallback = get_section_content(sections, ["降级链", "降级"], "")

    parts = []
    if fields:
        parts.append(f"## 📋 提供字段\n\n{fields}\n")
    else:
        parts.append("## 📋 提供字段\n\n待补充\n")

    if rate_limit:
        parts.append(f"## ⏱ 限流策略\n\n{rate_limit}\n")
    else:
        parts.append("## ⏱ 限流策略\n\n- 限流：`" + get_fm_field(fm, "rate_limit") + "`\n")

    if fallback:
        parts.append(f"## 🔄 降级链\n\n{fallback}\n")
    else:
        parts.append("## 🔄 降级链\n\n- 降级：`" + get_fm_field(fm, "fallback") + "`\n")

    parts.append("""## 🔗 相关实体

- [[stocks/]]
- [[reports/]]
- [[dragon-tiger/]]
- [[metrics/]]
- [[valuations/]]
- [[events/]]""")

    parts.append("""## 📜 关联 spec

- [[specs/]]""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_spec_body(fm: str, sections: dict) -> str:
    problem = get_section_content(sections, ["问题", "目标", "选择"], "")
    requirement = get_section_content(sections, ["需求", "理由", "核心改造"], "")
    affected = get_section_content(sections, ["受影响文件", "影响文件", "架构"], "")
    ac = get_section_content(sections, ["验收标准", "验收", "被否决", "关联"], "")

    parts = []
    if problem:
        parts.append(f"## 🎯 问题/目标\n\n{problem}\n")
    else:
        parts.append("## 🎯 问题/目标\n\n待补充\n")

    if requirement:
        parts.append(f"## 📝 需求\n\n{requirement}\n")
    else:
        parts.append("## 📝 需求\n\n待补充\n")

    if affected:
        parts.append(f"## 📂 受影响文件\n\n{affected}\n")
    else:
        parts.append("## 📂 受影响文件\n\n待补充\n")

    if ac:
        parts.append(f"## ✅ 验收标准\n\n{ac}\n")
    else:
        parts.append("## ✅ 验收标准\n\n- [ ] 待补充\n")

    parts.append("""## 🔗 关联决策

> 与其他 spec 的依赖/冲突/替代关系。

- [[specs/]]""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_decision_body(fm: str, sections: dict) -> str:
    choice = get_section_content(sections, ["选择", "决策"], "")
    reason = get_section_content(sections, ["理由"], "")
    rejected = get_section_content(sections, ["被否决", "否决"], "")
    related = get_section_content(sections, ["关联", "相关"], "")

    parts = []
    if choice:
        parts.append(f"## 🎯 决策\n\n{choice}\n")
    else:
        parts.append("## 🎯 决策\n\n待补充\n")

    if reason:
        parts.append(f"## 📝 理由\n\n{reason}\n")
    else:
        parts.append("## 📝 理由\n\n待补充\n")

    if rejected:
        parts.append(f"## ❌ 被否决方案\n\n{rejected}\n")
    else:
        parts.append("## ❌ 被否决方案\n\n无\n")

    if related:
        parts.append(f"## 🔗 关联\n\n{related}\n")
    else:
        parts.append("## 🔗 关联\n\n- [[specs/]]\n")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_project_body(fm: str, sections: dict) -> str:
    overview = get_section_content(sections, ["项目概述", "概述"], "")
    architecture = get_section_content(sections, ["架构", "核心改造"], "")
    related = get_section_content(sections, ["关联", "相关", "数据源"], "")

    parts = []
    if overview:
        parts.append(f"## 📋 项目概述\n\n{overview}\n")
    else:
        parts.append("## 📋 项目概述\n\n待补充\n")

    if architecture:
        parts.append(f"## 🏗 架构\n\n{architecture}\n")
    else:
        parts.append("## 🏗 架构\n\n待补充\n")

    if related:
        parts.append(f"## 🔗 关联\n\n{related}\n")
    else:
        parts.append("## 🔗 关联\n\n- [[specs/]]\n- [[data-sources/]]\n")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_agent_body(fm: str, sections: dict) -> str:
    role = get_section_content(sections, ["角色职责", "职责"], "")

    parts = []
    if role:
        parts.append(f"## 🎯 角色职责\n\n{role}\n")
    else:
        parts.append("## 🎯 角色职责\n\n待补充\n")

    parts.append("""## 📡 数据源

- [[data-sources/]]""")

    parts.append("""## ⚔️ 辩论对手

> 该 Agent 在 Bull/Bear 辩论与风险三方辩论中的对手角色。

- [[agents/]]""")

    parts.append("""## 🔗 与 Vibe-Research 的关系

> 该 Agent 与 Vibe-Research 项目的对应关系（数据源共享 / 工具复用 / 互补分析）。""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_dragon_tiger_body(fm: str, sections: dict) -> str:
    seats = get_section_content(sections, ["席位", "明细"], "")
    portrait = get_section_content(sections, ["游资画像", "画像"], "")

    parts = []
    if seats:
        parts.append(f"## 📊 席位明细\n\n{seats}\n")
    else:
        parts.append(f"## 📊 席位明细\n\n- 股票代码：`{get_fm_field(fm, 'code')}`\n- 日期：`{get_fm_field(fm, 'date')}`\n- 机构净额：`{get_fm_field(fm, 'institution_net')}`\n")

    if portrait:
        parts.append(f"## 🎭 游资画像\n\n{portrait}\n")
    else:
        parts.append("""## 🎭 游资画像

> 记录上榜席位的游资风格：一日游/趋势/接力/量化。""")

    parts.append("""## 📈 所属股票

```dataview
TABLE WITHOUT ID
  name AS "名称",
  industry AS "行业"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND code = this.code
```""")

    parts.append("""## ⚡ 相关事件

```dataview
TABLE WITHOUT ID
  date AS "日期",
  event_type AS "类型",
  summary AS "摘要"
FROM "10_Reference/investing/events"
WHERE type = "event" AND contains(codes, this.code) AND date = this.date
SORT date DESC
LIMIT 5
```""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_event_body(fm: str, sections: dict) -> str:
    overview = get_section_content(sections, ["事件概述", "概述", "涨停概览"], "")
    targets = get_section_content(sections, ["影响标的", "涨停标的"], "")

    parts = []
    if overview:
        parts.append(f"## 📋 事件概述\n\n{overview}\n")
    else:
        parts.append(f"## 📋 事件概述\n\n- 日期：`{get_fm_field(fm, 'date')}`\n- 类型：`{get_fm_field(fm, 'event_type')}`\n")

    parts.append("""## 🎯 影响标的

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  industry AS "行业"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND contains(this.codes, code)
SORT code ASC
LIMIT 30
```""")

    parts.append("""## ⚔️ 触发战法

> 该事件可能触发哪些战法？

- [[strategies/]]""")

    parts.append("""## 📰 连板梯队

> 涨停事件记录连板梯队（首板/2连板/3连板…）。""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_metric_body(fm: str, sections: dict) -> str:
    summary = get_section_content(sections, ["财务摘要", "摘要"], "")
    profit = get_section_content(sections, ["盈利能力"], "")

    parts = []
    if summary:
        parts.append(f"## 📊 财务摘要\n\n{summary}\n")
    else:
        parts.append(f"## 📊 财务摘要\n\n- 股票代码：`{get_fm_field(fm, 'code')}`\n- 报告期：`{get_fm_field(fm, 'period')}`\n")

    if profit:
        parts.append(f"## 📈 盈利能力\n\n{profit}\n")
    else:
        parts.append(f"## 📈 盈利能力\n\n- ROE：`{get_fm_field(fm, 'roe')}`%\n- 毛利率：`{get_fm_field(fm, 'gross_margin')}`%\n")

    parts.append("""## 📉 趋势

```dataview
TABLE WITHOUT ID
  period AS "周期",
  revenue AS "营收(亿)",
  net_profit AS "净利(亿)",
  roe AS "ROE%",
  gross_margin AS "毛利率%"
FROM "10_Reference/investing/metrics"
WHERE type = "metric" AND code = this.code
SORT period DESC
LIMIT 8
```""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_valuation_body(fm: str, sections: dict) -> str:
    snapshot = get_section_content(sections, ["估值快照", "估值指标", "快照"], "")
    percentile = get_section_content(sections, ["历史分位", "分位"], "")

    parts = []
    if snapshot:
        parts.append(f"## 💰 估值指标\n\n{snapshot}\n")
    else:
        parts.append(f"## 💰 估值指标\n\n- PE(TTM)：`{get_fm_field(fm, 'pe_ttm')}`\n- PB：`{get_fm_field(fm, 'pb')}`\n")

    if percentile:
        parts.append(f"## 📊 历史分位\n\n{percentile}\n")
    else:
        parts.append(f"## 📊 历史分位\n\n- PE 分位：`{get_fm_field(fm, 'pe_percentile')}`%\n- PB 分位：`{get_fm_field(fm, 'pb_percentile')}`%\n")

    parts.append("""## 📋 一致预期

- 一致预期 EPS：`consensus_eps`""")

    parts.append("""## 📉 历史估值序列

```dataview
TABLE WITHOUT ID
  created AS "日期",
  pe_ttm AS "PE(TTM)",
  pb AS "PB",
  pe_percentile AS "PE分位%",
  pb_percentile AS "PB分位%"
FROM "10_Reference/investing/valuations"
WHERE type = "valuation" AND code = this.code
SORT created DESC
LIMIT 10
```""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_report_body(fm: str, sections: dict) -> str:
    summary = get_section_content(sections, ["报告摘要", "摘要"], "")
    viewpoint = get_section_content(sections, ["核心观点", "观点"], "")
    rating = get_section_content(sections, ["评级", "目标价"], "")

    parts = []
    if summary:
        parts.append(f"## 📋 报告摘要\n\n{summary}\n")
    else:
        parts.append(f"## 📋 报告摘要\n\n- 标题：`{get_fm_field(fm, 'title')}`\n- 机构：`{get_fm_field(fm, 'org')}`\n")

    if viewpoint:
        parts.append(f"## 💡 核心观点\n\n{viewpoint}\n")
    else:
        parts.append("## 💡 核心观点\n\n待补充\n")

    parts.append("""## 🎯 覆盖标的

```dataview
TABLE WITHOUT ID
  name AS "名称",
  industry AS "行业",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND code = this.code
```""")

    parts.append("""## 👤 分析师其他研报

```dataview
TABLE WITHOUT ID
  title AS "标题",
  publish_date AS "日期",
  rating_change AS "评级"
FROM "10_Reference/investing/reports"
WHERE type = "report" AND researcher = this.researcher AND title != this.title
SORT publish_date DESC
LIMIT 10
```""")

    if rating:
        parts.append(f"## 📊 评级与目标价\n\n{rating}\n")
    else:
        parts.append(f"## 📊 评级与目标价\n\n- 评级变动：`{get_fm_field(fm, 'rating_change')}`\n- 目标价：`{get_fm_field(fm, 'target_price')}`\n")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_analyst_body(fm: str, sections: dict) -> str:
    coverage = get_section_content(sections, ["覆盖领域", "覆盖"], "")

    parts = []
    if coverage:
        parts.append(f"## 📋 覆盖领域\n\n{coverage}\n")
    else:
        parts.append("## 📋 覆盖领域\n\n待补充\n")

    parts.append("""## 📰 近期研报

```dataview
TABLE WITHOUT ID
  title AS "标题",
  code AS "标的",
  publish_date AS "日期",
  rating_change AS "评级",
  target_price AS "目标价"
FROM "10_Reference/investing/reports"
WHERE type = "report" AND contains(researcher, this.name) AND org = this.org
SORT publish_date DESC
LIMIT 10
```""")

    parts.append(f"## 🏢 机构\n\n- 所属：`{get_fm_field(fm, 'org')}`\n")

    parts.append("""## 📊 历史评级胜率

> 手动跟踪或后续 LLM 推断填充：该分析师历史评级后续涨跌统计。""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_index_body(fm: str, sections: dict) -> str:
    overview = get_section_content(sections, ["指数概览", "概览"], "")

    parts = []
    if overview:
        parts.append(f"## 📋 指数概览\n\n{overview}\n")
    else:
        parts.append(f"## 📋 指数概览\n\n- 指数代码：`{get_fm_field(fm, 'code')}`\n- 名称：{get_fm_field(fm, 'name')}\n")

    parts.append("""## 🏢 成分股

```dataview
TABLE WITHOUT ID
  code AS "代码",
  name AS "名称",
  industry AS "行业",
  market_cap AS "市值"
FROM "10_Reference/investing/stocks"
WHERE type = "stock" AND contains(indices, this.code)
SORT market_cap DESC
LIMIT 30
```""")

    parts.append("""## 📈 近期走势

> 链接 K 线数据源或粘贴关键点位。""")

    parts.append(build_relation_footer())
    return "\n\n".join(parts)


def build_logic_body(fm: str, sections: dict) -> str:
    definition = get_section_content(sections, ["规则定义", "定义"], "")
    trigger = get_section_content(sections, ["触发条件", "触发"], "")
    execution = get_section_content(sections, ["执行逻辑", "执行"], "")
    violation = get_section_content(sections, ["违反处置", "违反", "处置"], "")

    parts = []
    if definition:
        parts.append(f"## 📋 规则定义\n\n{definition}\n")
    else:
        parts.append(f"## 📋 规则定义\n\n- 类型：`{get_fm_field(fm, 'rule_type')}`\n- 适用实体：`{get_fm_field(fm, 'target_entity')}`\n- 严重级：`{get_fm_field(fm, 'severity')}`\n")

    if trigger:
        parts.append(f"## ⚡ 触发条件\n\n{trigger}\n")
    else:
        parts.append("## ⚡ 触发条件\n\n待补充\n")

    if execution:
        parts.append(f"## 🔧 执行逻辑\n\n{execution}\n")
    else:
        parts.append("## 🔧 执行逻辑\n\n待补充\n")

    if violation:
        parts.append(f"## ⚠️ 违反处置\n\n{violation}\n")
    else:
        parts.append(f"## ⚠️ 违反处置\n\n- `{get_fm_field(fm, 'action_on_violation')}`\n")

    parts.append("""## 🔗 关联

- **触发动作**：[[actions/]]
- **约束实体**：[[stocks/]]
- **来源决策**：[[specs/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个""")
    return "\n\n".join(parts)


def build_action_body(fm: str, sections: dict) -> str:
    definition = get_section_content(sections, ["动作定义", "定义"], "")
    steps = get_section_content(sections, ["执行步骤", "步骤"], "")
    audit = get_section_content(sections, ["审计点", "审计"], "")

    parts = []
    if definition:
        parts.append(f"## 📋 动作定义\n\n{definition}\n")
    else:
        parts.append(f"## 📋 动作定义\n\n- 类型：`{get_fm_field(fm, 'action_type')}`\n- 触发：`{get_fm_field(fm, 'trigger')}`\n- 目标：`{get_fm_field(fm, 'target')}`\n")

    if steps:
        parts.append(f"## 🔧 执行步骤\n\n{steps}\n")
    else:
        parts.append("## 🔧 执行步骤\n\n1. 待补充\n")

    if audit:
        parts.append(f"## 🔍 审计点\n\n{audit}\n")
    else:
        parts.append("## 🔍 审计点\n\n- 执行前状态：\n- 执行后状态：\n- 异常处置：\n")

    parts.append("""## 🔗 关联

- **触发自**：[[logic/]]
- **作用于**：[[stocks/]]
- **执行记录**：[[reviews/]]
- **出链**：`=(length(this.file.outlinks))` 个 · **入链**：`=(length(this.file.inlinks))` 个""")
    return "\n\n".join(parts)


# 各类型 body 构建器映射
BODY_BUILDERS = {
    "industry":     build_industry_body,
    "concept":      build_concept_body,
    "data_source":  build_data_source_body,
    "spec":         build_spec_body,
    "decision":     build_decision_body,
    "project":      build_project_body,
    "agent_role":   build_agent_body,
    "dragon_tiger": build_dragon_tiger_body,
    "event":        build_event_body,
    "metric":       build_metric_body,
    "valuation":    build_valuation_body,
    "report":       build_report_body,
    "analyst":      build_analyst_body,
    "index":        build_index_body,
    "logic":        build_logic_body,
    "action":       build_action_body,
}


def update_entity(filepath: Path, fm_type: str, emoji: str, callout_title: str,
                  dry_run: bool = False) -> bool:
    """更新单个实体文件。"""
    fm, body = parse_file(filepath)
    if fm is None:
        print(f"  ⚠️  跳过（无 frontmatter）: {filepath.name}")
        return False

    # 检查 type 是否匹配
    actual_type = get_fm_field(fm, "type")
    if actual_type != fm_type:
        return False

    builder = BODY_BUILDERS.get(fm_type)
    if not builder:
        return False

    sections = extract_body_sections(body)
    callout = build_callout(fm, fm_type, emoji, callout_title)
    new_body = builder(fm, sections)

    new_content = f"---\n{fm}\n---\n\n{callout}\n\n{new_body}\n"

    if dry_run:
        return True

    filepath.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="批量更新所有实体类型格式")
    parser.add_argument("--dry-run", action="store_true", help="只预览不写盘")
    parser.add_argument("types", nargs="*", help="指定实体类型（如 industries concepts），默认全量")
    args = parser.parse_args()

    if args.types:
        types_to_process = {k: v for k, v in ENTITY_TYPES.items() if k in args.types}
        if not types_to_process:
            print(f"未知类型: {args.types}")
            print(f"可选: {list(ENTITY_TYPES.keys())}")
            return 1
    else:
        types_to_process = ENTITY_TYPES

    total_count = 0
    for folder_name, (fm_type, emoji, callout_title) in types_to_process.items():
        entity_dir = VAULT / folder_name
        if not entity_dir.exists():
            print(f"⚠️  文件夹不存在: {folder_name}")
            continue

        # specs 文件夹包含 spec/decision/project 三种类型
        if folder_name == "specs":
            accepted_types = {"spec", "decision", "project"}
        else:
            accepted_types = {fm_type}

        count = 0
        skipped = 0
        for f in sorted(entity_dir.glob("*.md")):
            if f.name == "index.md":
                continue
            if f.name == "SUMMARY.md":
                continue
            try:
                fm, body = parse_file(f)
                if fm is None:
                    print(f"  ⚠️  跳过（无 frontmatter）: {f.name}")
                    skipped += 1
                    continue
                actual_type = get_fm_field(fm, "type")
                if actual_type not in accepted_types:
                    skipped += 1
                    continue
                builder = BODY_BUILDERS.get(actual_type)
                if not builder:
                    skipped += 1
                    continue
                sections = extract_body_sections(body)
                callout = build_callout(fm, actual_type, emoji, callout_title)
                new_body = builder(fm, sections)
                new_content = f"---\n{fm}\n---\n\n{callout}\n\n{new_body}\n"
                if not args.dry_run:
                    f.write_text(new_content, encoding="utf-8")
                count += 1
            except Exception as e:
                print(f"  ❌ 错误 {f.name}: {e}")
                skipped += 1

        total_count += count
        status = "（dry-run）" if args.dry_run else ""
        print(f"✅ {folder_name}: {count} 个更新 {status}" + (f"，{skipped} 跳过" if skipped else ""))

    print(f"\n总计更新 {total_count} 个实体" + ("（dry-run，未写盘）" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
