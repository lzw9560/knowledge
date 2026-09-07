# 估值 索引

> 个股估值快照与历史分位节点。对应 Pydantic 契约 `Valuation` + `ValuationPercentile`。每条记录链接其所属股票、历史估值序列、一致预期。

## 实体列表（Dataview 动态）

```dataview
TABLE code AS "股票代码", pe_ttm AS "PE(TTM)", pb AS "PB", peg AS "PEG", pe_percentile AS "PE分位%", pb_percentile AS "PB分位%", dividend_yield AS "股息率%"
FROM "valuations"
WHERE type = "valuation"
SORT code ASC, created DESC
```


## 实体清单（入边）

> 本段列出实体以建立入边链接（Dataview 表格不计入边）。

- [[valuations/000001-latest]] · [[valuations/000002-latest]] · [[valuations/000009-latest]] · [[valuations/000021-latest]] · [[valuations/000027-latest]]
- [[valuations/000032-latest]] · [[valuations/000034-latest]] · [[valuations/000039-latest]] · [[valuations/000050-latest]] · [[valuations/000060-latest]]
- [[valuations/000062-latest]] · [[valuations/000063-latest]] · [[valuations/000088-latest]] · [[valuations/000100-latest]] · [[valuations/000155-latest]]
- [[valuations/000157-latest]] · [[valuations/000166-latest]] · [[valuations/000301-latest]] · [[valuations/000333-latest]] · [[valuations/000338-latest]]
- [[valuations/000400-latest]] · [[valuations/000408-latest]] · [[valuations/000415-latest]] · [[valuations/000423-latest]] · [[valuations/000425-latest]]
- [[valuations/000428-latest]] · [[valuations/000429-latest]] · [[valuations/000513-latest]] · [[valuations/000519-latest]] · [[valuations/000528-latest]]
- [[valuations/000537-latest]] · [[valuations/000538-latest]] · [[valuations/000539-latest]] · [[valuations/000559-latest]] · [[valuations/000560-latest]]
- [[valuations/000568-latest]] · [[valuations/000582-latest]] · [[valuations/000591-latest]] · [[valuations/000592-latest]] · [[valuations/000596-latest]]
- [[valuations/000598-latest]] · [[valuations/000617-latest]] · [[valuations/000623-latest]] · [[valuations/000625-latest]] · [[valuations/000629-latest]]
- [[valuations/000630-latest]] · [[valuations/000635-latest]] · [[valuations/000636-latest]] · [[valuations/000651-latest]] · [[valuations/000657-latest]]
- [[valuations/000661-latest]] · [[valuations/000683-latest]] · [[valuations/000703-latest]] · [[valuations/000708-latest]] · [[valuations/000709-latest]]
- [[valuations/000725-latest]] · [[valuations/000768-latest]] · [[valuations/000776-latest]] · [[valuations/000792-latest]] · [[valuations/000798-latest]]
- [[valuations/000807-latest]] · [[valuations/000858-latest]] · [[valuations/000892-latest]] · [[valuations/000895-latest]] · [[valuations/000938-latest]]
- [[valuations/000963-latest]] · [[valuations/000975-latest]] · [[valuations/000977-latest]] · [[valuations/000988-latest]] · [[valuations/000999-latest]]
- [[valuations/001280-latest]] · [[valuations/001330-latest]] · [[valuations/001366-latest]] · [[valuations/001391-latest]] · [[valuations/001965-latest]]
- [[valuations/001979-latest]] · [[valuations/002001-latest]] · [[valuations/002027-latest]] · [[valuations/002028-latest]] · [[valuations/002049-latest]]
- [[valuations/002050-latest]] · [[valuations/002059-latest]] · [[valuations/002074-latest]] · [[valuations/002084-latest]] · [[valuations/002104-latest]]
- [[valuations/002124-latest]] · [[valuations/002142-latest]] · [[valuations/002156-latest]] · [[valuations/002179-latest]] · [[valuations/002185-latest]]
- [[valuations/002202-latest]] · [[valuations/002230-latest]] · [[valuations/002236-latest]] · [[valuations/002241-latest]] · [[valuations/002281-latest]]
- [[valuations/002297-latest]] · [[valuations/002300-latest]] · [[valuations/002304-latest]] · [[valuations/002311-latest]] · [[valuations/002352-latest]]
- [[valuations/002353-latest]] · [[valuations/002354-latest]] · [[valuations/002371-latest]] · [[valuations/002384-latest]] · [[valuations/002403-latest]]
- [[valuations/002415-latest]] · [[valuations/002422-latest]] · [[valuations/002428-latest]] · [[valuations/002460-latest]] · [[valuations/002463-latest]]
- [[valuations/002466-latest]] · [[valuations/002475-latest]] · [[valuations/002484-latest]] · [[valuations/002493-latest]] · [[valuations/002532-latest]]
- [[valuations/002558-latest]] · [[valuations/002564-latest]] · [[valuations/002594-latest]] · [[valuations/002600-latest]] · [[valuations/002602-latest]]
- [[valuations/002625-latest]] · [[valuations/002636-latest]] · [[valuations/002648-latest]] · [[valuations/002679-latest]] · [[valuations/002702-latest]]
- [[valuations/002708-latest]] · [[valuations/002709-latest]] · [[valuations/002714-latest]] · [[valuations/002736-latest]] · [[valuations/002827-latest]]
- [[valuations/002837-latest]] · [[valuations/002855-latest]] · [[valuations/002868-latest]] · [[valuations/002909-latest]] · [[valuations/002916-latest]]
- [[valuations/002920-latest]] · [[valuations/002938-latest]] · [[valuations/003005-latest]] · [[valuations/003040-latest]] · [[valuations/003816-latest]]
- [[valuations/300014-latest]] · [[valuations/300015-latest]] · [[valuations/300033-latest]] · [[valuations/300058-latest]] · [[valuations/300059-latest]]
- [[valuations/300124-latest]] · [[valuations/300274-latest]] · [[valuations/300308-latest]] · [[valuations/300316-latest]] · [[valuations/300394-latest]]
- [[valuations/300408-latest]] · [[valuations/300413-latest]] · [[valuations/300418-latest]] · [[valuations/300433-latest]] · [[valuations/300442-latest]]
- [[valuations/300450-latest]] · [[valuations/300476-latest]] · [[valuations/300498-latest]] · [[valuations/300502-latest]] · [[valuations/300661-latest]]
- [[valuations/300750-latest]] · [[valuations/300760-latest]] · [[valuations/300803-latest]] · [[valuations/300866-latest]] · [[valuations/301165-latest]]
- [[valuations/301217-latest]] · [[valuations/301269-latest]] · [[valuations/301308-latest]] · [[valuations/301511-latest]] · [[valuations/600000-latest]]
- [[valuations/600009-latest]] · [[valuations/600010-latest]] · [[valuations/600011-latest]] · [[valuations/600015-latest]] · [[valuations/600016-latest]]
- [[valuations/600018-latest]] · [[valuations/600019-latest]] · [[valuations/600023-latest]] · [[valuations/600025-latest]] · [[valuations/600026-latest]]
- [[valuations/600027-latest]] · [[valuations/600028-latest]] · [[valuations/600029-latest]] · [[valuations/600030-latest]] · [[valuations/600031-latest]]
- [[valuations/600036-latest]] · [[valuations/600039-latest]] · [[valuations/600048-latest]] · [[valuations/600050-latest]] · [[valuations/600059-latest]]
- [[valuations/600061-latest]] · [[valuations/600066-latest]] · [[valuations/600089-latest]] · [[valuations/600104-latest]] · [[valuations/600108-latest]]
- [[valuations/600111-latest]] · [[valuations/600115-latest]] · [[valuations/600118-latest]] · [[valuations/600121-latest]] · [[valuations/600127-latest]]
- [[valuations/600150-latest]] · [[valuations/600160-latest]] · [[valuations/600176-latest]] · [[valuations/600183-latest]] · [[valuations/600188-latest]]
- [[valuations/600196-latest]] · [[valuations/600206-latest]] · [[valuations/600219-latest]] · [[valuations/600221-latest]] · [[valuations/600233-latest]]
- [[valuations/600276-latest]] · [[valuations/600309-latest]] · [[valuations/600346-latest]] · [[valuations/600354-latest]] · [[valuations/600362-latest]]
- [[valuations/600371-latest]] · [[valuations/600372-latest]] · [[valuations/600406-latest]] · [[valuations/600415-latest]] · [[valuations/600426-latest]]
- [[valuations/600436-latest]] · [[valuations/600438-latest]] · [[valuations/600460-latest]] · [[valuations/600482-latest]] · [[valuations/600489-latest]]
- [[valuations/600506-latest]] · [[valuations/600519-latest]] · [[valuations/600522-latest]] · [[valuations/600540-latest]] · [[valuations/600547-latest]]
- [[valuations/600549-latest]] · [[valuations/600551-latest]] · [[valuations/600570-latest]] · [[valuations/600584-latest]] · [[valuations/600585-latest]]
- [[valuations/600611-latest]] · [[valuations/600657-latest]] · [[valuations/600660-latest]] · [[valuations/600674-latest]] · [[valuations/600690-latest]]
- [[valuations/600698-latest]] · [[valuations/600726-latest]] · [[valuations/600741-latest]] · [[valuations/600760-latest]] · [[valuations/600795-latest]]
- [[valuations/600802-latest]] · [[valuations/600803-latest]] · [[valuations/600809-latest]] · [[valuations/600828-latest]] · [[valuations/600830-latest]]
- [[valuations/600865-latest]] · [[valuations/600869-latest]] · [[valuations/600875-latest]] · [[valuations/600886-latest]] · [[valuations/600887-latest]]
- [[valuations/600892-latest]] · [[valuations/600893-latest]] · [[valuations/600900-latest]] · [[valuations/600905-latest]] · [[valuations/600919-latest]]
- [[valuations/600926-latest]] · [[valuations/600930-latest]] · [[valuations/600938-latest]] · [[valuations/600941-latest]] · [[valuations/600958-latest]]
- [[valuations/600967-latest]] · [[valuations/600989-latest]] · [[valuations/600999-latest]] · [[valuations/601006-latest]] · [[valuations/601009-latest]]
- [[valuations/601012-latest]] · [[valuations/601018-latest]] · [[valuations/601021-latest]] · [[valuations/601058-latest]] · [[valuations/601059-latest]]
- [[valuations/601066-latest]] · [[valuations/601077-latest]] · [[valuations/601086-latest]] · [[valuations/601088-latest]] · [[valuations/601100-latest]]
- [[valuations/601111-latest]] · [[valuations/601117-latest]] · [[valuations/601127-latest]] · [[valuations/601136-latest]] · [[valuations/601138-latest]]
- [[valuations/601166-latest]] · [[valuations/601169-latest]] · [[valuations/601186-latest]] · [[valuations/601208-latest]] · [[valuations/601211-latest]]
- [[valuations/601225-latest]] · [[valuations/601229-latest]] · [[valuations/601288-latest]] · [[valuations/601318-latest]] · [[valuations/601319-latest]]
- [[valuations/601328-latest]] · [[valuations/601336-latest]] · [[valuations/601360-latest]] · [[valuations/601377-latest]] · [[valuations/601390-latest]]
- [[valuations/601398-latest]] · [[valuations/601566-latest]] · [[valuations/601579-latest]] · [[valuations/601600-latest]] · [[valuations/601601-latest]]
- [[valuations/601607-latest]] · [[valuations/601618-latest]] · [[valuations/601628-latest]] · [[valuations/601633-latest]] · [[valuations/601658-latest]]
- [[valuations/601668-latest]] · [[valuations/601669-latest]] · [[valuations/601688-latest]] · [[valuations/601689-latest]] · [[valuations/601698-latest]]
- [[valuations/601727-latest]] · [[valuations/601728-latest]] · [[valuations/601766-latest]] · [[valuations/601788-latest]] · [[valuations/601800-latest]]
- [[valuations/601816-latest]] · [[valuations/601818-latest]] · [[valuations/601825-latest]] · [[valuations/601838-latest]] · [[valuations/601857-latest]]
- [[valuations/601868-latest]] · [[valuations/601872-latest]] · [[valuations/601877-latest]] · [[valuations/601878-latest]] · [[valuations/601881-latest]]
- [[valuations/601888-latest]] · [[valuations/601898-latest]] · [[valuations/601899-latest]] · [[valuations/601901-latest]] · [[valuations/601916-latest]]
- [[valuations/601919-latest]] · [[valuations/601939-latest]] · [[valuations/601949-latest]] · [[valuations/601985-latest]] · [[valuations/601988-latest]]
- [[valuations/601995-latest]] · [[valuations/601998-latest]] · [[valuations/603019-latest]] · [[valuations/603083-latest]] · [[valuations/603122-latest]]
- [[valuations/603123-latest]] · [[valuations/603151-latest]] · [[valuations/603162-latest]] · [[valuations/603207-latest]] · [[valuations/603259-latest]]
- [[valuations/603270-latest]] · [[valuations/603288-latest]] · [[valuations/603296-latest]] · [[valuations/603390-latest]] · [[valuations/603501-latest]]
- [[valuations/603533-latest]] · [[valuations/603696-latest]] · [[valuations/603721-latest]] · [[valuations/603799-latest]] · [[valuations/603893-latest]]
- [[valuations/603986-latest]] · [[valuations/603993-latest]] · [[valuations/605117-latest]] · [[valuations/605398-latest]] · [[valuations/605499-latest]]
- [[valuations/605577-latest]] · [[valuations/605580-latest]] · [[valuations/688008-latest]] · [[valuations/688009-latest]] · [[valuations/688012-latest]]
- [[valuations/688036-latest]] · [[valuations/688041-latest]] · [[valuations/688047-latest]] · [[valuations/688048-latest]] · [[valuations/688072-latest]]
- [[valuations/688082-latest]] · [[valuations/688110-latest]] · [[valuations/688111-latest]] · [[valuations/688126-latest]] · [[valuations/688141-latest]]
- [[valuations/688147-latest]] · [[valuations/688167-latest]] · [[valuations/688183-latest]] · [[valuations/688223-latest]] · [[valuations/688256-latest]]
- [[valuations/688271-latest]] · [[valuations/688300-latest]] · [[valuations/688396-latest]] · [[valuations/688409-latest]] · [[valuations/688432-latest]]
- [[valuations/688433-latest]] · [[valuations/688506-latest]] · [[valuations/688519-latest]] · [[valuations/688521-latest]] · [[valuations/688536-latest]]
- [[valuations/688548-latest]] · [[valuations/688627-latest]] · [[valuations/688630-latest]] · [[valuations/688766-latest]] · [[valuations/688836-latest]]
- [[valuations/688981-latest]]

## 关系

- belongs_to: [[stocks/]]（每条估值数据所属股票）
- pairs_with: [[metrics/]]（估值与财务配对看，PE = 股价 / EPS）
- consensus: [[reports/]]（一致预期 EPS 来自研报）
- sourced_from: [[data-sources/]]（估值数据来源）

## 新建实体

用 Templater 应用 `templates/valuation` 新建。模板 frontmatter 对应 `Valuation` + `ValuationPercentile` 字段（pe_ttm/pb/ps_ttm/pcf_ttm/dividend_yield/peg/forward_pe/consensus_eps/pe_percentile/pb_percentile）。

---

## ⚡ 快速操作

用 Templater 应用 `templates/valuation` 新建 估值 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

```dataview
TABLE WITHOUT ID
  length(rows) AS "估值总数"
FROM "10_Reference/investing/valuations"
WHERE type = "valuation" AND file.name != "index"
```

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
