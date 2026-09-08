# 行业板块 索引

> 证监会行业分类节点。对应 Pydantic 契约 `IndustrySector`。每个行业链接其成分股、相关概念、近期事件、资金流向。

## 实体列表（Dataview 动态）

<!-- dataview-precompiled:f15fcb5a2c2f -->
| 行业代码 | 行业名称 | 分类来源 |
|---|---|---|
| — | IT服务 | 东财涨停池行业分类 |
| — | 一般零售 | 东财涨停池行业分类 |
| — | 专用设备 | 东财涨停池行业分类 |
| — | 养殖业 | 东财涨停池行业分类 |
| — | 出版 | 东财涨停池行业分类 |
| — | 动物保健 | 东财涨停池行业分类 |
| — | 化学制品 | 东财涨停池行业分类 |
| — | 化学制药 | 东财涨停池行业分类 |
| — | 化学原料 | 东财涨停池行业分类 |
| — | 医疗服务 | 东财涨停池行业分类 |
| — | 地面兵装 | 东财涨停池行业分类 |
| — | 多元金融 | 东财涨停池行业分类 |
| — | 家居用品 | 东财涨停池行业分类 |
| — | 小家电 | 东财涨停池行业分类 |
| — | 影视院线 | 东财涨停池行业分类 |
| — | 房地产开发 | 东财涨停池行业分类 |
| — | 房地产服务 | 东财涨停池行业分类 |
| — | 数字媒体 | 东财涨停池行业分类 |
| — | 旅游及景区 | 东财涨停池行业分类 |
| — | 服装家纺 | 东财涨停池行业分类 |
| — | 林业 | 东财涨停池行业分类 |
| — | 水泥 | 东财涨停池行业分类 |
| — | 汽车零部件 | 东财涨停池行业分类 |
| — | 消费电子 | 东财涨停池行业分类 |
| — | 渔业 | 东财涨停池行业分类 |
| — | 游戏 | 东财涨停池行业分类 |
| — | 炼化及贸易 | 东财涨停池行业分类 |
| — | 煤炭开采 | 东财涨停池行业分类 |
| — | 环保 | LLM推断（由待核实行业股票业务描述推断） |
| — | 电网设备 | 东财涨停池行业分类 |
| — | 种植业 | 东财涨停池行业分类 |
| — | 航空装备 | 东财涨停池行业分类 |
| — | 航运港口 | 东财涨停池行业分类 |
| — | 调味发酵品 | 东财涨停池行业分类 |
| — | 通用设备 | 东财涨停池行业分类 |
| — | 酒店餐饮 | 东财涨停池行业分类 |
| — | 铅锌 | LLM推断（由待核实行业股票业务描述推断） |
| — | 非白酒 | 东财涨停池行业分类 |
| — | 食品加工 | 东财涨停池行业分类 |
| — | 饲料 | 东财涨停池行业分类 |
| A01 | 农业 | 证监会行业分类 |
| A03 | 养殖 | 东方财富EM2016行业分类 |
| B06 | 煤炭开采洗选 | 东方财富EM2016行业分类 |
| B07 | 油田服务 | 东方财富EM2016行业分类 |
| B07 | 石油天然气开采 | 东方财富EM2016行业分类 |
| B09 | 其他稀有小金属 | 东方财富EM2016行业分类 |
| B09 | 稀土 | 东方财富EM2016行业分类 |
| B09 | 钨 | 东方财富EM2016行业分类 |
| B09 | 铜 | 东方财富EM2016行业分类 |
| B09 | 铝 | 东方财富EM2016行业分类 |
<!-- /dataview-precompiled -->

## 关系

- has_members: [[10_Reference/investing/stocks/index|stocks/]]（行业下成分股）
- related_to: [[10_Reference/investing/concepts/index|concepts/]]（行业相关概念题材）
- has_events: [[10_Reference/investing/events/index|events/]]（行业级事件）
- covered_by: [[10_Reference/investing/reports/index|reports/]]（行业研报）
- sourced_from: [[10_Reference/investing/data-sources/index|data-sources/]]（行业分类来源）

## 新建实体

用 Templater 应用 `templates/industry` 新建。模板会自动填入 YAML frontmatter（code/name/source）+ 正文骨架（行业概览/成分股/资金流向/相关概念/近期事件）。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/industries/IT服务]]
- [[10_Reference/investing/industries/PC、服务器及硬件]]
- [[10_Reference/investing/industries/一般零售]]
- [[10_Reference/investing/industries/专业工程]]
- [[10_Reference/investing/industries/专用计算机设备]]
- [[10_Reference/investing/industries/专用设备]]
- [[10_Reference/investing/industries/中药生产]]
- [[10_Reference/investing/industries/乘用车]]
- [[10_Reference/investing/industries/交通运输]]
- [[10_Reference/investing/industries/传媒]]
- [[10_Reference/investing/industries/保健护理产品]]
- [[10_Reference/investing/industries/保险]]
- [[10_Reference/investing/industries/储能设备]]
- [[10_Reference/investing/industries/光学元件]]
- [[10_Reference/investing/industries/其他互联网服务]]
- [[10_Reference/investing/industries/其他互联网金融]]
- [[10_Reference/investing/industries/其他基础建设]]
- [[10_Reference/investing/industries/其他电子器件]]
- [[10_Reference/investing/industries/其他稀有小金属]]
- [[10_Reference/investing/industries/其他软件服务]]
- [[10_Reference/investing/industries/其他输变电设备]]
- [[10_Reference/investing/industries/其他非银行金融]]
- [[10_Reference/investing/industries/养殖]]
- [[10_Reference/investing/industries/养殖业]]
- [[10_Reference/investing/industries/农业]]
- [[10_Reference/investing/industries/出版]]
- [[10_Reference/investing/industries/动物保健]]
- [[10_Reference/investing/industries/化学制品]]
- [[10_Reference/investing/industries/化学制药]]
- [[10_Reference/investing/industries/化学原料]]
- [[10_Reference/investing/industries/化学新材料]]
- [[10_Reference/investing/industries/医疗器械]]
- [[10_Reference/investing/industries/医疗服务]]
- [[10_Reference/investing/industries/医药商业]]
- [[10_Reference/investing/industries/半导体]]
- [[10_Reference/investing/industries/半导体封测]]
- [[10_Reference/investing/industries/商用车]]
- [[10_Reference/investing/industries/国有银行]]
- [[10_Reference/investing/industries/地面兵装]]
- [[10_Reference/investing/industries/基础软件]]
- [[10_Reference/investing/industries/多元金融]]
- [[10_Reference/investing/industries/太阳能]]
- [[10_Reference/investing/industries/家居用品]]
- [[10_Reference/investing/industries/小家电]]
- [[10_Reference/investing/industries/影视院线]]
- [[10_Reference/investing/industries/待核实]]
- [[10_Reference/investing/industries/房地产开发]]
- [[10_Reference/investing/industries/房地产服务]]
- [[10_Reference/investing/industries/房屋建筑]]
- [[10_Reference/investing/industries/数字媒体]]
- [[10_Reference/investing/industries/旅游及景区]]
- [[10_Reference/investing/industries/显示器件]]
- [[10_Reference/investing/industries/普钢]]
- [[10_Reference/investing/industries/智能卡]]
- [[10_Reference/investing/industries/服装家纺]]
- [[10_Reference/investing/industries/机器人]]
- [[10_Reference/investing/industries/林业]]
- [[10_Reference/investing/industries/氮肥]]
- [[10_Reference/investing/industries/水利建设]]
- [[10_Reference/investing/industries/水泥]]
- [[10_Reference/investing/industries/汽车整车]]
- [[10_Reference/investing/industries/汽车零部件]]
- [[10_Reference/investing/industries/油田服务]]
- [[10_Reference/investing/industries/消费电子]]
- [[10_Reference/investing/industries/消费电子设备]]
- [[10_Reference/investing/industries/渔业]]
- [[10_Reference/investing/industries/游戏]]
- [[10_Reference/investing/industries/游戏娱乐]]
- [[10_Reference/investing/industries/炼化及贸易]]
- [[10_Reference/investing/industries/煤炭开采]]
- [[10_Reference/investing/industries/煤炭开采洗选]]
- [[10_Reference/investing/industries/燃气]]
- [[10_Reference/investing/industries/特钢]]
- [[10_Reference/investing/industries/环保]]
- [[10_Reference/investing/industries/玻纤]]
- [[10_Reference/investing/industries/生物医药]]
- [[10_Reference/investing/industries/电力]]
- [[10_Reference/investing/industries/电力设备]]
- [[10_Reference/investing/industries/电子元件]]
- [[10_Reference/investing/industries/电子设备制造]]
- [[10_Reference/investing/industries/电气自控设备]]
- [[10_Reference/investing/industries/电池]]
- [[10_Reference/investing/industries/电池材料]]
- [[10_Reference/investing/industries/电线电缆]]
- [[10_Reference/investing/industries/电网设备]]
- [[10_Reference/investing/industries/白色家电]]
- [[10_Reference/investing/industries/白酒]]
- [[10_Reference/investing/industries/石油加工]]
- [[10_Reference/investing/industries/石油天然气开采]]
- [[10_Reference/investing/industries/种植业]]
- [[10_Reference/investing/industries/稀土]]
- [[10_Reference/investing/industries/综合电力设备商]]
- [[10_Reference/investing/industries/网络媒体]]
- [[10_Reference/investing/industries/股份制与城商行]]
- [[10_Reference/investing/industries/航天装备]]
- [[10_Reference/investing/industries/航空装备]]
- [[10_Reference/investing/industries/航运港口]]
- [[10_Reference/investing/industries/船舶制造]]
- [[10_Reference/investing/industries/营销服务]]
- [[10_Reference/investing/industries/行业应用软件]]
- [[10_Reference/investing/industries/证券]]
- [[10_Reference/investing/industries/调味发酵品]]
- [[10_Reference/investing/industries/贸易]]
- [[10_Reference/investing/industries/路桥建设]]
- [[10_Reference/investing/industries/轨道交通设备]]
- [[10_Reference/investing/industries/轮胎]]
- [[10_Reference/investing/industries/软件]]
- [[10_Reference/investing/industries/通信设备]]
- [[10_Reference/investing/industries/通信运营]]
- [[10_Reference/investing/industries/通用设备]]
- [[10_Reference/investing/industries/酒店餐饮]]
- [[10_Reference/investing/industries/钨]]
- [[10_Reference/investing/industries/钾肥]]
- [[10_Reference/investing/industries/铁路城轨建设]]
- [[10_Reference/investing/industries/铁路车辆及动车组]]
- [[10_Reference/investing/industries/铅锌]]
- [[10_Reference/investing/industries/铜]]
- [[10_Reference/investing/industries/铝]]
- [[10_Reference/investing/industries/锂]]
- [[10_Reference/investing/industries/零售]]
- [[10_Reference/investing/industries/非白酒]]
- [[10_Reference/investing/industries/风能]]
- [[10_Reference/investing/industries/食品加工]]
- [[10_Reference/investing/industries/食品饮料]]
- [[10_Reference/investing/industries/饲料]]
- [[10_Reference/investing/industries/黄金]]


---

## ⚡ 快速操作

用 Templater 应用 `templates/industry` 新建 行业板块 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:fa4bc848d4cc -->
| 行业板块总数 |
|---|
| 126 |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
