# 行业板块 索引

> 证监会行业分类节点。对应 Pydantic 契约 `IndustrySector`。每个行业链接其成分股、相关概念、近期事件、资金流向。

## 实体列表（Dataview 动态）

```dataview
TABLE WITHOUT ID
  code AS "行业代码", name AS "行业名称", source AS "分类来源"
FROM "10_Reference/investing/industries"
WHERE type = "industry" AND file.name != "index"
SORT code ASC
LIMIT 50
```

## 关系

- has_members: [[stocks/]]（行业下成分股）
- related_to: [[concepts/]]（行业相关概念题材）
- has_events: [[events/]]（行业级事件）
- covered_by: [[reports/]]（行业研报）
- sourced_from: [[data-sources/]]（行业分类来源）

## 新建实体

用 Templater 应用 `templates/industry` 新建。模板会自动填入 YAML frontmatter（code/name/source）+ 正文骨架（行业概览/成分股/资金流向/相关概念/近期事件）。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[industries/IT服务]]
- [[industries/PC、服务器及硬件]]
- [[industries/一般零售]]
- [[industries/专业工程]]
- [[industries/专用计算机设备]]
- [[industries/专用设备]]
- [[industries/中药生产]]
- [[industries/乘用车]]
- [[industries/交通运输]]
- [[industries/传媒]]
- [[industries/保健护理产品]]
- [[industries/保险]]
- [[industries/储能设备]]
- [[industries/光学元件]]
- [[industries/其他互联网服务]]
- [[industries/其他互联网金融]]
- [[industries/其他基础建设]]
- [[industries/其他电子器件]]
- [[industries/其他稀有小金属]]
- [[industries/其他软件服务]]
- [[industries/其他输变电设备]]
- [[industries/其他非银行金融]]
- [[industries/养殖]]
- [[industries/养殖业]]
- [[industries/农业]]
- [[industries/出版]]
- [[industries/动物保健]]
- [[industries/化学制品]]
- [[industries/化学制药]]
- [[industries/化学原料]]
- [[industries/化学新材料]]
- [[industries/医疗器械]]
- [[industries/医疗服务]]
- [[industries/医药商业]]
- [[industries/半导体]]
- [[industries/半导体封测]]
- [[industries/商用车]]
- [[industries/国有银行]]
- [[industries/地面兵装]]
- [[industries/基础软件]]
- [[industries/多元金融]]
- [[industries/太阳能]]
- [[industries/家居用品]]
- [[industries/小家电]]
- [[industries/影视院线]]
- [[industries/待核实]]
- [[industries/房地产开发]]
- [[industries/房地产服务]]
- [[industries/房屋建筑]]
- [[industries/数字媒体]]
- [[industries/旅游及景区]]
- [[industries/显示器件]]
- [[industries/普钢]]
- [[industries/智能卡]]
- [[industries/服装家纺]]
- [[industries/机器人]]
- [[industries/林业]]
- [[industries/氮肥]]
- [[industries/水利建设]]
- [[industries/水泥]]
- [[industries/汽车整车]]
- [[industries/汽车零部件]]
- [[industries/油田服务]]
- [[industries/消费电子]]
- [[industries/消费电子设备]]
- [[industries/渔业]]
- [[industries/游戏]]
- [[industries/游戏娱乐]]
- [[industries/炼化及贸易]]
- [[industries/煤炭开采]]
- [[industries/煤炭开采洗选]]
- [[industries/燃气]]
- [[industries/特钢]]
- [[industries/环保]]
- [[industries/玻纤]]
- [[industries/生物医药]]
- [[industries/电力]]
- [[industries/电力设备]]
- [[industries/电子元件]]
- [[industries/电子设备制造]]
- [[industries/电气自控设备]]
- [[industries/电池]]
- [[industries/电池材料]]
- [[industries/电线电缆]]
- [[industries/电网设备]]
- [[industries/白色家电]]
- [[industries/白酒]]
- [[industries/石油加工]]
- [[industries/石油天然气开采]]
- [[industries/种植业]]
- [[industries/稀土]]
- [[industries/综合电力设备商]]
- [[industries/网络媒体]]
- [[industries/股份制与城商行]]
- [[industries/航天装备]]
- [[industries/航空装备]]
- [[industries/航运港口]]
- [[industries/船舶制造]]
- [[industries/营销服务]]
- [[industries/行业应用软件]]
- [[industries/证券]]
- [[industries/调味发酵品]]
- [[industries/贸易]]
- [[industries/路桥建设]]
- [[industries/轨道交通设备]]
- [[industries/轮胎]]
- [[industries/软件]]
- [[industries/通信设备]]
- [[industries/通信运营]]
- [[industries/通用设备]]
- [[industries/酒店餐饮]]
- [[industries/钨]]
- [[industries/钾肥]]
- [[industries/铁路城轨建设]]
- [[industries/铁路车辆及动车组]]
- [[industries/铅锌]]
- [[industries/铜]]
- [[industries/铝]]
- [[industries/锂]]
- [[industries/零售]]
- [[industries/非白酒]]
- [[industries/风能]]
- [[industries/食品加工]]
- [[industries/食品饮料]]
- [[industries/饲料]]
- [[industries/黄金]]


---

## ⚡ 快速操作

用 Templater 应用 `templates/industry` 新建 行业板块 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "行业板块总数"
FROM "10_Reference/investing/industries"
WHERE type = "industry" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
