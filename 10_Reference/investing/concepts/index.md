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

- has_members: [[stocks/]]（概念下成分股）
- related_to: [[industries/]]（概念关联的行业）
- has_events: [[events/]]（概念级催化事件）
- covered_by: [[reports/]]（概念研报）
- triggers_strategies: [[strategies/]]（题材轮动触发的战法，如龙头战法）

## 新建实体

用 Templater 应用 `templates/concept` 新建。模板侧重题材轮动节奏记录。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[concepts/5G概念]]
- [[concepts/AIGC]]
- [[concepts/AIOps]]
- [[concepts/AI应用]]
- [[concepts/AI眼镜]]
- [[concepts/AI硬件]]
- [[concepts/CPO]]
- [[concepts/CPO概念]]
- [[concepts/DeepSeek概念]]
- [[concepts/F5G概念]]
- [[concepts/IPO受益]]
- [[concepts/IPv6]]
- [[concepts/IT运维]]
- [[concepts/MicroLED]]
- [[concepts/MiniLED]]
- [[concepts/OLED]]
- [[concepts/PCB]]
- [[concepts/一带一路]]
- [[concepts/东数西算]]
- [[concepts/云计算]]
- [[concepts/互联网医疗]]
- [[concepts/互联网金融]]
- [[concepts/人工智能]]
- [[concepts/人形机器人]]
- [[concepts/传媒]]
- [[concepts/低空经济]]
- [[concepts/信创]]
- [[concepts/储能概念]]
- [[concepts/元宇宙概念]]
- [[concepts/充电桩]]
- [[concepts/先进封装]]
- [[concepts/光伏概念]]
- [[concepts/光模块]]
- [[concepts/光纤光缆]]
- [[concepts/光纤概念]]
- [[concepts/光通信模块]]
- [[concepts/养老金]]
- [[concepts/军工]]
- [[concepts/农化制品]]
- [[concepts/农林牧渔]]
- [[concepts/净水概念]]
- [[concepts/出租车]]
- [[concepts/创投]]
- [[concepts/券商概念]]
- [[concepts/动力电池]]
- [[concepts/区块链]]
- [[concepts/医疗器械概念]]
- [[concepts/半导体]]
- [[concepts/半导体概念]]
- [[concepts/华为概念]]
- [[concepts/参股券商]]
- [[concepts/反内卷概念]]
- [[concepts/味蕾经济]]
- [[concepts/商业百货]]
- [[concepts/商业航天]]
- [[concepts/固态电池]]
- [[concepts/国产芯片]]
- [[concepts/国产软件]]
- [[concepts/国资改革]]
- [[concepts/在线教育]]
- [[concepts/大农业]]
- [[concepts/大数据]]
- [[concepts/安防概念]]
- [[concepts/小米概念]]
- [[concepts/小金属概念]]
- [[concepts/屏下摄像]]
- [[concepts/工业互联网]]
- [[concepts/工业母机]]
- [[concepts/数字经济]]
- [[concepts/数字货币]]
- [[concepts/数据中心]]
- [[concepts/新材料]]
- [[concepts/新能源]]
- [[concepts/新能源发电]]
- [[concepts/新能源车]]
- [[concepts/新零售]]
- [[concepts/无线耳机]]
- [[concepts/显示技术]]
- [[concepts/智慧城市]]
- [[concepts/智慧能源]]
- [[concepts/智能家居]]
- [[concepts/智能穿戴]]
- [[concepts/智能驾驶]]
- [[concepts/有色金属]]
- [[concepts/机器人]]
- [[concepts/机器人概念]]
- [[concepts/柔性屏(折叠屏)]]
- [[concepts/比亚迪产业链]]
- [[concepts/氢能源]]
- [[concepts/消费复苏]]
- [[concepts/消费电子概念]]
- [[concepts/涨停池]]
- [[concepts/液冷服务器]]
- [[concepts/游戏]]
- [[concepts/热电]]
- [[concepts/燃料电池概念]]
- [[concepts/物联网]]
- [[concepts/特斯拉概念]]
- [[concepts/玻璃基板]]
- [[concepts/电子纸概念]]
- [[concepts/电池技术]]
- [[concepts/白酒]]
- [[concepts/白酒龙头]]
- [[concepts/稀缺资源]]
- [[concepts/空气能热泵]]
- [[concepts/算力概念]]
- [[concepts/粮食]]
- [[concepts/网约车]]
- [[concepts/网络安全]]
- [[concepts/节能环保]]
- [[concepts/英伟达概念]]
- [[concepts/苹果概念]]
- [[concepts/营销]]
- [[concepts/虚拟现实]]
- [[concepts/资源]]
- [[concepts/超清视频]]
- [[concepts/跨境支付]]
- [[concepts/车联网(车路云)]]
- [[concepts/边缘计算]]
- [[concepts/通信技术]]
- [[concepts/量子科技]]
- [[concepts/铜]]
- [[concepts/铜缆]]
- [[concepts/锂电池概念]]
- [[concepts/锂电铜箔]]
- [[concepts/锂矿概念]]
- [[concepts/风能]]
- [[concepts/食品饮料]]
- [[concepts/高端白酒]]
- [[concepts/黄金]]

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
