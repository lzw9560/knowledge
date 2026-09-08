# 概念板块 索引

> 概念题材板块节点。对应 Pydantic 契约 `ConceptBlock` + `Sector`。每个概念链接其成分股、题材轮动节奏、相关研报、近期事件。

## 实体列表（Dataview 动态）

```dataview
TABLE WITHOUT ID
  code AS "概念代码", name AS "概念名称", related_industry AS "关联行业"
FROM "10_Reference/investing/concepts"
WHERE type = "concept" AND file.name != "index"
SORT name ASC
LIMIT 50
```

## 关系

- has_members: [[10_Reference/investing/stocks/index|stocks/]]（概念下成分股）
- related_to: [[10_Reference/investing/industries/index|industries/]]（概念关联的行业）
- has_events: [[10_Reference/investing/events/index|events/]]（概念级催化事件）
- covered_by: [[10_Reference/investing/reports/index|reports/]]（概念研报）
- triggers_strategies: [[10_Reference/investing/strategies/index|strategies/]]（题材轮动触发的战法，如龙头战法）

## 新建实体

用 Templater 应用 `templates/concept` 新建。模板侧重题材轮动节奏记录。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/concepts/5G概念]]
- [[10_Reference/investing/concepts/AIGC]]
- [[10_Reference/investing/concepts/AIOps]]
- [[10_Reference/investing/concepts/AI应用]]
- [[10_Reference/investing/concepts/AI眼镜]]
- [[10_Reference/investing/concepts/AI硬件]]
- [[10_Reference/investing/concepts/CPO]]
- [[10_Reference/investing/concepts/CPO概念]]
- [[10_Reference/investing/concepts/DeepSeek概念]]
- [[10_Reference/investing/concepts/F5G概念]]
- [[10_Reference/investing/concepts/IPO受益]]
- [[10_Reference/investing/concepts/IPv6]]
- [[10_Reference/investing/concepts/IT运维]]
- [[10_Reference/investing/concepts/MicroLED]]
- [[10_Reference/investing/concepts/MiniLED]]
- [[10_Reference/investing/concepts/OLED]]
- [[10_Reference/investing/concepts/PCB]]
- [[10_Reference/investing/concepts/一带一路]]
- [[10_Reference/investing/concepts/东数西算]]
- [[10_Reference/investing/concepts/云计算]]
- [[10_Reference/investing/concepts/互联网医疗]]
- [[10_Reference/investing/concepts/互联网金融]]
- [[10_Reference/investing/concepts/人工智能]]
- [[10_Reference/investing/concepts/人形机器人]]
- [[10_Reference/investing/concepts/传媒]]
- [[10_Reference/investing/concepts/低空经济]]
- [[10_Reference/investing/concepts/信创]]
- [[10_Reference/investing/concepts/储能概念]]
- [[10_Reference/investing/concepts/元宇宙概念]]
- [[10_Reference/investing/concepts/充电桩]]
- [[10_Reference/investing/concepts/先进封装]]
- [[10_Reference/investing/concepts/光伏概念]]
- [[10_Reference/investing/concepts/光模块]]
- [[10_Reference/investing/concepts/光纤光缆]]
- [[10_Reference/investing/concepts/光纤概念]]
- [[10_Reference/investing/concepts/光通信模块]]
- [[10_Reference/investing/concepts/养老金]]
- [[10_Reference/investing/concepts/军工]]
- [[10_Reference/investing/concepts/农化制品]]
- [[10_Reference/investing/concepts/农林牧渔]]
- [[10_Reference/investing/concepts/净水概念]]
- [[10_Reference/investing/concepts/出租车]]
- [[10_Reference/investing/concepts/创投]]
- [[10_Reference/investing/concepts/券商概念]]
- [[10_Reference/investing/concepts/动力电池]]
- [[10_Reference/investing/concepts/区块链]]
- [[10_Reference/investing/concepts/医疗器械概念]]
- [[10_Reference/investing/concepts/半导体]]
- [[10_Reference/investing/concepts/半导体概念]]
- [[10_Reference/investing/concepts/华为概念]]
- [[10_Reference/investing/concepts/参股券商]]
- [[10_Reference/investing/concepts/反内卷概念]]
- [[10_Reference/investing/concepts/味蕾经济]]
- [[10_Reference/investing/concepts/商业百货]]
- [[10_Reference/investing/concepts/商业航天]]
- [[10_Reference/investing/concepts/固态电池]]
- [[10_Reference/investing/concepts/国产芯片]]
- [[10_Reference/investing/concepts/国产软件]]
- [[10_Reference/investing/concepts/国资改革]]
- [[10_Reference/investing/concepts/在线教育]]
- [[10_Reference/investing/concepts/大农业]]
- [[10_Reference/investing/concepts/大数据]]
- [[10_Reference/investing/concepts/安防概念]]
- [[10_Reference/investing/concepts/小米概念]]
- [[10_Reference/investing/concepts/小金属概念]]
- [[10_Reference/investing/concepts/屏下摄像]]
- [[10_Reference/investing/concepts/工业互联网]]
- [[10_Reference/investing/concepts/工业母机]]
- [[10_Reference/investing/concepts/数字经济]]
- [[10_Reference/investing/concepts/数字货币]]
- [[10_Reference/investing/concepts/数据中心]]
- [[10_Reference/investing/concepts/新材料]]
- [[10_Reference/investing/concepts/新能源]]
- [[10_Reference/investing/concepts/新能源发电]]
- [[10_Reference/investing/concepts/新能源车]]
- [[10_Reference/investing/concepts/新零售]]
- [[10_Reference/investing/concepts/无线耳机]]
- [[10_Reference/investing/concepts/显示技术]]
- [[10_Reference/investing/concepts/智慧城市]]
- [[10_Reference/investing/concepts/智慧能源]]
- [[10_Reference/investing/concepts/智能家居]]
- [[10_Reference/investing/concepts/智能穿戴]]
- [[10_Reference/investing/concepts/智能驾驶]]
- [[10_Reference/investing/concepts/有色金属]]
- [[10_Reference/investing/concepts/机器人]]
- [[10_Reference/investing/concepts/机器人概念]]
- [[10_Reference/investing/concepts/柔性屏(折叠屏)]]
- [[10_Reference/investing/concepts/比亚迪产业链]]
- [[10_Reference/investing/concepts/氢能源]]
- [[10_Reference/investing/concepts/消费复苏]]
- [[10_Reference/investing/concepts/消费电子概念]]
- [[10_Reference/investing/concepts/涨停池]]
- [[10_Reference/investing/concepts/液冷服务器]]
- [[10_Reference/investing/concepts/游戏]]
- [[10_Reference/investing/concepts/热电]]
- [[10_Reference/investing/concepts/燃料电池概念]]
- [[10_Reference/investing/concepts/物联网]]
- [[10_Reference/investing/concepts/特斯拉概念]]
- [[10_Reference/investing/concepts/玻璃基板]]
- [[10_Reference/investing/concepts/电子纸概念]]
- [[10_Reference/investing/concepts/电池技术]]
- [[10_Reference/investing/concepts/白酒]]
- [[10_Reference/investing/concepts/白酒龙头]]
- [[10_Reference/investing/concepts/稀缺资源]]
- [[10_Reference/investing/concepts/空气能热泵]]
- [[10_Reference/investing/concepts/算力概念]]
- [[10_Reference/investing/concepts/粮食]]
- [[10_Reference/investing/concepts/网约车]]
- [[10_Reference/investing/concepts/网络安全]]
- [[10_Reference/investing/concepts/节能环保]]
- [[10_Reference/investing/concepts/英伟达概念]]
- [[10_Reference/investing/concepts/苹果概念]]
- [[10_Reference/investing/concepts/营销]]
- [[10_Reference/investing/concepts/虚拟现实]]
- [[10_Reference/investing/concepts/资源]]
- [[10_Reference/investing/concepts/超清视频]]
- [[10_Reference/investing/concepts/跨境支付]]
- [[10_Reference/investing/concepts/车联网(车路云)]]
- [[10_Reference/investing/concepts/边缘计算]]
- [[10_Reference/investing/concepts/通信技术]]
- [[10_Reference/investing/concepts/量子科技]]
- [[10_Reference/investing/concepts/铜]]
- [[10_Reference/investing/concepts/铜缆]]
- [[10_Reference/investing/concepts/锂电池概念]]
- [[10_Reference/investing/concepts/锂电铜箔]]
- [[10_Reference/investing/concepts/锂矿概念]]
- [[10_Reference/investing/concepts/风能]]
- [[10_Reference/investing/concepts/食品饮料]]
- [[10_Reference/investing/concepts/高端白酒]]
- [[10_Reference/investing/concepts/黄金]]

---

## ⚡ 快速操作

用 Templater 应用 `templates/concept` 新建 概念板块 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "概念板块总数"
FROM "10_Reference/investing/concepts"
WHERE type = "concept" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
