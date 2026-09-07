# 财务指标 索引

> 个股财务周期数据节点。对应 Pydantic 契约 `Financials` + `FinancialPeriod`。每条记录链接其所属股票、趋势、盈利能力。

## 实体列表（Dataview 动态）

```dataview
TABLE WITHOUT ID
  code AS "股票代码", period AS "报告期", revenue AS "营收(亿)", net_profit AS "净利(亿)", roe AS "ROE%", gross_margin AS "毛利率%", eps AS "EPS"
FROM "10_Reference/investing/metrics"
WHERE type = "metric" AND file.name != "index"
SORT code ASC, period DESC
LIMIT 50
```


## 实体清单（入边）

> 本段列出实体以建立入边链接（Dataview 表格不计入边）。

- [[metrics/000001-latest]] · [[metrics/000002-latest]] · [[metrics/000009-latest]] · [[metrics/000021-latest]] · [[metrics/000027-latest]]
- [[metrics/000032-latest]] · [[metrics/000034-latest]] · [[metrics/000039-latest]] · [[metrics/000050-latest]] · [[metrics/000060-latest]]
- [[metrics/000062-latest]] · [[metrics/000063-latest]] · [[metrics/000088-latest]] · [[metrics/000100-latest]] · [[metrics/000155-latest]]
- [[metrics/000157-latest]] · [[metrics/000166-latest]] · [[metrics/000301-latest]] · [[metrics/000333-latest]] · [[metrics/000338-latest]]
- [[metrics/000400-latest]] · [[metrics/000408-latest]] · [[metrics/000415-latest]] · [[metrics/000423-latest]] · [[metrics/000425-latest]]
- [[metrics/000428-latest]] · [[metrics/000429-latest]] · [[metrics/000513-latest]] · [[metrics/000519-latest]] · [[metrics/000528-latest]]
- [[metrics/000537-latest]] · [[metrics/000538-latest]] · [[metrics/000539-latest]] · [[metrics/000559-latest]] · [[metrics/000560-latest]]
- [[metrics/000568-latest]] · [[metrics/000582-latest]] · [[metrics/000591-latest]] · [[metrics/000592-latest]] · [[metrics/000596-latest]]
- [[metrics/000598-latest]] · [[metrics/000617-latest]] · [[metrics/000623-latest]] · [[metrics/000625-latest]] · [[metrics/000629-latest]]
- [[metrics/000630-latest]] · [[metrics/000635-latest]] · [[metrics/000636-latest]] · [[metrics/000651-latest]] · [[metrics/000657-latest]]
- [[metrics/000661-latest]] · [[metrics/000683-latest]] · [[metrics/000703-latest]] · [[metrics/000708-latest]] · [[metrics/000709-latest]]
- [[metrics/000725-latest]] · [[metrics/000768-latest]] · [[metrics/000776-latest]] · [[metrics/000792-latest]] · [[metrics/000798-latest]]
- [[metrics/000807-latest]] · [[metrics/000858-latest]] · [[metrics/000892-latest]] · [[metrics/000895-latest]] · [[metrics/000938-latest]]
- [[metrics/000963-latest]] · [[metrics/000975-latest]] · [[metrics/000977-latest]] · [[metrics/000988-latest]] · [[metrics/000999-latest]]
- [[metrics/001280-latest]] · [[metrics/001330-latest]] · [[metrics/001366-latest]] · [[metrics/001391-latest]] · [[metrics/001965-latest]]
- [[metrics/001979-latest]] · [[metrics/002001-latest]] · [[metrics/002027-latest]] · [[metrics/002028-latest]] · [[metrics/002049-latest]]
- [[metrics/002050-latest]] · [[metrics/002059-latest]] · [[metrics/002074-latest]] · [[metrics/002084-latest]] · [[metrics/002104-latest]]
- [[metrics/002124-latest]] · [[metrics/002142-latest]] · [[metrics/002156-latest]] · [[metrics/002179-latest]] · [[metrics/002185-latest]]
- [[metrics/002202-latest]] · [[metrics/002230-latest]] · [[metrics/002236-latest]] · [[metrics/002241-latest]] · [[metrics/002281-latest]]
- [[metrics/002297-latest]] · [[metrics/002300-latest]] · [[metrics/002304-latest]] · [[metrics/002311-latest]] · [[metrics/002352-latest]]
- [[metrics/002353-latest]] · [[metrics/002354-latest]] · [[metrics/002371-latest]] · [[metrics/002384-latest]] · [[metrics/002403-latest]]
- [[metrics/002415-latest]] · [[metrics/002422-latest]] · [[metrics/002428-latest]] · [[metrics/002460-latest]] · [[metrics/002463-latest]]
- [[metrics/002466-latest]] · [[metrics/002475-latest]] · [[metrics/002484-latest]] · [[metrics/002493-latest]] · [[metrics/002532-latest]]
- [[metrics/002558-latest]] · [[metrics/002564-latest]] · [[metrics/002594-latest]] · [[metrics/002600-latest]] · [[metrics/002602-latest]]
- [[metrics/002625-latest]] · [[metrics/002636-latest]] · [[metrics/002648-latest]] · [[metrics/002679-latest]] · [[metrics/002702-latest]]
- [[metrics/002708-latest]] · [[metrics/002709-latest]] · [[metrics/002714-latest]] · [[metrics/002736-latest]] · [[metrics/002827-latest]]
- [[metrics/002837-latest]] · [[metrics/002855-latest]] · [[metrics/002868-latest]] · [[metrics/002909-latest]] · [[metrics/002916-latest]]
- [[metrics/002920-latest]] · [[metrics/002938-latest]] · [[metrics/003005-latest]] · [[metrics/003040-latest]] · [[metrics/003816-latest]]
- [[metrics/300014-latest]] · [[metrics/300015-latest]] · [[metrics/300033-latest]] · [[metrics/300058-latest]] · [[metrics/300059-latest]]
- [[metrics/300124-latest]] · [[metrics/300274-latest]] · [[metrics/300308-latest]] · [[metrics/300316-latest]] · [[metrics/300394-latest]]
- [[metrics/300408-latest]] · [[metrics/300413-latest]] · [[metrics/300418-latest]] · [[metrics/300433-latest]] · [[metrics/300442-latest]]
- [[metrics/300450-latest]] · [[metrics/300476-latest]] · [[metrics/300498-latest]] · [[metrics/300502-latest]] · [[metrics/300661-latest]]
- [[metrics/300750-latest]] · [[metrics/300760-latest]] · [[metrics/300803-latest]] · [[metrics/300866-latest]] · [[metrics/301165-latest]]
- [[metrics/301217-latest]] · [[metrics/301269-latest]] · [[metrics/301308-latest]] · [[metrics/301511-latest]] · [[metrics/600000-latest]]
- [[metrics/600009-latest]] · [[metrics/600010-latest]] · [[metrics/600011-latest]] · [[metrics/600015-latest]] · [[metrics/600016-latest]]
- [[metrics/600018-latest]] · [[metrics/600019-latest]] · [[metrics/600023-latest]] · [[metrics/600025-latest]] · [[metrics/600026-latest]]
- [[metrics/600027-latest]] · [[metrics/600028-latest]] · [[metrics/600029-latest]] · [[metrics/600030-latest]] · [[metrics/600031-latest]]
- [[metrics/600036-latest]] · [[metrics/600039-latest]] · [[metrics/600048-latest]] · [[metrics/600050-latest]] · [[metrics/600059-latest]]
- [[metrics/600061-latest]] · [[metrics/600066-latest]] · [[metrics/600089-latest]] · [[metrics/600104-latest]] · [[metrics/600108-latest]]
- [[metrics/600111-latest]] · [[metrics/600115-latest]] · [[metrics/600118-latest]] · [[metrics/600121-latest]] · [[metrics/600127-latest]]
- [[metrics/600150-latest]] · [[metrics/600160-latest]] · [[metrics/600176-latest]] · [[metrics/600183-latest]] · [[metrics/600188-latest]]
- [[metrics/600196-latest]] · [[metrics/600206-latest]] · [[metrics/600219-latest]] · [[metrics/600221-latest]] · [[metrics/600233-latest]]
- [[metrics/600276-latest]] · [[metrics/600309-latest]] · [[metrics/600346-latest]] · [[metrics/600354-latest]] · [[metrics/600362-latest]]
- [[metrics/600371-latest]] · [[metrics/600372-latest]] · [[metrics/600406-latest]] · [[metrics/600415-latest]] · [[metrics/600426-latest]]
- [[metrics/600436-latest]] · [[metrics/600438-latest]] · [[metrics/600460-latest]] · [[metrics/600482-latest]] · [[metrics/600489-latest]]
- [[metrics/600506-latest]] · [[metrics/600519-latest]] · [[metrics/600522-latest]] · [[metrics/600540-latest]] · [[metrics/600547-latest]]
- [[metrics/600549-latest]] · [[metrics/600551-latest]] · [[metrics/600570-latest]] · [[metrics/600584-latest]] · [[metrics/600585-latest]]
- [[metrics/600611-latest]] · [[metrics/600657-latest]] · [[metrics/600660-latest]] · [[metrics/600674-latest]] · [[metrics/600690-latest]]
- [[metrics/600698-latest]] · [[metrics/600726-latest]] · [[metrics/600741-latest]] · [[metrics/600760-latest]] · [[metrics/600795-latest]]
- [[metrics/600802-latest]] · [[metrics/600803-latest]] · [[metrics/600809-latest]] · [[metrics/600828-latest]] · [[metrics/600830-latest]]
- [[metrics/600865-latest]] · [[metrics/600869-latest]] · [[metrics/600875-latest]] · [[metrics/600886-latest]] · [[metrics/600887-latest]]
- [[metrics/600892-latest]] · [[metrics/600893-latest]] · [[metrics/600900-latest]] · [[metrics/600905-latest]] · [[metrics/600919-latest]]
- [[metrics/600926-latest]] · [[metrics/600930-latest]] · [[metrics/600938-latest]] · [[metrics/600941-latest]] · [[metrics/600958-latest]]
- [[metrics/600967-latest]] · [[metrics/600989-latest]] · [[metrics/600999-latest]] · [[metrics/601006-latest]] · [[metrics/601009-latest]]
- [[metrics/601012-latest]] · [[metrics/601018-latest]] · [[metrics/601021-latest]] · [[metrics/601058-latest]] · [[metrics/601059-latest]]
- [[metrics/601066-latest]] · [[metrics/601077-latest]] · [[metrics/601086-latest]] · [[metrics/601088-latest]] · [[metrics/601100-latest]]
- [[metrics/601111-latest]] · [[metrics/601117-latest]] · [[metrics/601127-latest]] · [[metrics/601136-latest]] · [[metrics/601138-latest]]
- [[metrics/601166-latest]] · [[metrics/601169-latest]] · [[metrics/601186-latest]] · [[metrics/601208-latest]] · [[metrics/601211-latest]]
- [[metrics/601225-latest]] · [[metrics/601229-latest]] · [[metrics/601288-latest]] · [[metrics/601318-latest]] · [[metrics/601319-latest]]
- [[metrics/601328-latest]] · [[metrics/601336-latest]] · [[metrics/601360-latest]] · [[metrics/601377-latest]] · [[metrics/601390-latest]]
- [[metrics/601398-latest]] · [[metrics/601566-latest]] · [[metrics/601579-latest]] · [[metrics/601600-latest]] · [[metrics/601601-latest]]
- [[metrics/601607-latest]] · [[metrics/601618-latest]] · [[metrics/601628-latest]] · [[metrics/601633-latest]] · [[metrics/601658-latest]]
- [[metrics/601668-latest]] · [[metrics/601669-latest]] · [[metrics/601688-latest]] · [[metrics/601689-latest]] · [[metrics/601698-latest]]
- [[metrics/601727-latest]] · [[metrics/601728-latest]] · [[metrics/601766-latest]] · [[metrics/601788-latest]] · [[metrics/601800-latest]]
- [[metrics/601816-latest]] · [[metrics/601818-latest]] · [[metrics/601825-latest]] · [[metrics/601838-latest]] · [[metrics/601857-latest]]
- [[metrics/601868-latest]] · [[metrics/601872-latest]] · [[metrics/601877-latest]] · [[metrics/601878-latest]] · [[metrics/601881-latest]]
- [[metrics/601888-latest]] · [[metrics/601898-latest]] · [[metrics/601899-latest]] · [[metrics/601901-latest]] · [[metrics/601916-latest]]
- [[metrics/601919-latest]] · [[metrics/601939-latest]] · [[metrics/601949-latest]] · [[metrics/601985-latest]] · [[metrics/601988-latest]]
- [[metrics/601995-latest]] · [[metrics/601998-latest]] · [[metrics/603019-latest]] · [[metrics/603083-latest]] · [[metrics/603122-latest]]
- [[metrics/603123-latest]] · [[metrics/603151-latest]] · [[metrics/603162-latest]] · [[metrics/603207-latest]] · [[metrics/603259-latest]]
- [[metrics/603270-latest]] · [[metrics/603288-latest]] · [[metrics/603296-latest]] · [[metrics/603390-latest]] · [[metrics/603501-latest]]
- [[metrics/603533-latest]] · [[metrics/603696-latest]] · [[metrics/603721-latest]] · [[metrics/603799-latest]] · [[metrics/603893-latest]]
- [[metrics/603986-latest]] · [[metrics/603993-latest]] · [[metrics/605117-latest]] · [[metrics/605398-latest]] · [[metrics/605499-latest]]
- [[metrics/605577-latest]] · [[metrics/605580-latest]] · [[metrics/688008-latest]] · [[metrics/688009-latest]] · [[metrics/688012-latest]]
- [[metrics/688036-latest]] · [[metrics/688041-latest]] · [[metrics/688047-latest]] · [[metrics/688048-latest]] · [[metrics/688072-latest]]
- [[metrics/688082-latest]] · [[metrics/688110-latest]] · [[metrics/688111-latest]] · [[metrics/688126-latest]] · [[metrics/688141-latest]]
- [[metrics/688147-latest]] · [[metrics/688167-latest]] · [[metrics/688183-latest]] · [[metrics/688223-latest]] · [[metrics/688256-latest]]
- [[metrics/688271-latest]] · [[metrics/688300-latest]] · [[metrics/688396-latest]] · [[metrics/688409-latest]] · [[metrics/688432-latest]]
- [[metrics/688433-latest]] · [[metrics/688506-latest]] · [[metrics/688519-latest]] · [[metrics/688521-latest]] · [[metrics/688536-latest]]
- [[metrics/688548-latest]] · [[metrics/688627-latest]] · [[metrics/688630-latest]] · [[metrics/688766-latest]] · [[metrics/688836-latest]]
- [[metrics/688981-latest]]

## 关系

- belongs_to: [[stocks/]]（每条财务数据所属股票）
- pairs_with: [[valuations/]]（财务与估值配对看）
- sourced_from: [[data-sources/]]（财务数据来源，如东方财富/同花顺）

## 新建实体

用 Templater 应用 `templates/metric` 新建。模板 frontmatter 对应 `Financials` 字段（revenue/net_profit/roe/gross_margin/net_margin/eps/bvps/op_cf_ps）。

---

## ⚡ 快速操作

用 Templater 应用 `templates/metric` 新建 财务指标 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "财务指标总数"
FROM "10_Reference/investing/metrics"
WHERE type = "metric" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
