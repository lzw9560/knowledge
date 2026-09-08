---
type: methodology_index
name: 元知识层
domain: 通用
created: 2026-09-07
---
# 估值 索引

> 个股估值快照与历史分位节点。对应 Pydantic 契约 `Valuation` + `ValuationPercentile`。每条记录链接其所属股票、历史估值序列、一致预期。

## 实体列表（Dataview 动态）

<!-- dataview-precompiled:5aa423118be5 -->
| 股票代码 | PE(TTM) | PB | PEG | PE分位% | PB分位% | 股息率% |
|---|---|---|---|---|---|---|
| 000001 | 5.22 | 0.48 | 1.46 | 61.8 | 21.6 | — |
| 000002 | -0.42 | 0.37 | — | 36.5 | 20.4 | — |
| 000009 | -258.37 | 1.87 | — | 0.4 | 3.4 | — |
| 000021 | 45.57 | 4.2 | 1.1 | 75.4 | 93.5 | — |
| 000027 | 12.98 | 0.89 | — | 16.4 | 2.1 | — |
| 000032 | -72.41 | 2.38 | 0.89 | 27.1 | 3.7 | — |
| 000034 | 40.58 | 2.1 | 0.99 | 71.8 | 28.8 | — |
| 000039 | -159.66 | 1.11 | 0.41 | 6.8 | 78.1 | — |
| 000050 | -20.98 | 0.61 | 0.6 | 29.8 | 4.2 | — |
| 000060 | 20.68 | 1.41 | 2.15 | 62.0 | 65.1 | — |
| 000062 | 40.65 | 3.65 | 4.01 | 59.6 | 68.9 | — |
| 000063 | 48.05 | 2.11 | 1.51 | 99.2 | 31.0 | — |
| 000088 | 15.87 | 1.31 | — | 18.5 | 52.4 | — |
| 000100 | 16.39 | 1.69 | 0.32 | 32.9 | 68.3 | — |
| 000155 | 24.57 | 1.98 | 0.71 | 31.4 | 15.3 | — |
| 000157 | 13.69 | 1.0 | 0.47 | 20.3 | 20.7 | — |
| 000166 | 10.33 | 0.98 | 1.51 | 0.0 | 1.9 | — |
| 000301 | 21.7 | 2.43 | 1.99 | 48.1 | 62.2 | — |
| 000333 | 14.83 | 3.11 | 1.76 | 84.9 | 85.0 | — |
| 000338 | 18.32 | 2.48 | 0.69 | 73.8 | 92.0 | — |
| 000400 | 23.55 | 1.81 | 0.73 | 31.2 | 7.3 | — |
| 000408 | 20.41 | 7.43 | 0.58 | 54.2 | 84.6 | — |
| 000415 | 5.76 | 0.89 | — | 70.9 | 89.4 | — |
| 000423 | 16.94 | 3.25 | 1.1 | 1.9 | 36.3 | — |
| 000425 | 15.76 | 1.56 | 0.42 | 58.3 | 54.7 | — |
| 000428 | -24.26 | 4.29 | — | 7.7 | 100.0 | — |
| 000429 | 16.93 | 2.55 | 12.91 | 88.5 | 87.6 | — |
| 000513 | 14.4 | 1.8 | 1.01 | 5.9 | 0.8 | — |
| 000519 | 182.67 | 2.1 | 0.98 | 99.7 | 27.7 | — |
| 000528 | 11.39 | 0.87 | 0.35 | 15.7 | 29.6 | — |
| 000537 | 32.36 | 0.77 | 0.68 | 87.3 | 0.8 | — |
| 000538 | 17.28 | 2.2 | 2.02 | 4.8 | 8.1 | — |
| 000539 | 1229.85 | 1.17 | — | 99.3 | 55.6 | — |
| 000559 | 34.73 | 4.43 | 2.76 | 80.0 | 86.2 | — |
| 000560 | -135.93 | 0.79 | 1.57 | 6.8 | 84.0 | — |
| 000568 | 15.55 | 2.55 | 2.48 | 42.5 | 4.5 | — |
| 000582 | 28.55 | 1.48 | 1.21 | 97.3 | 95.7 | — |
| 000591 | 26.43 | 0.69 | 2.15 | 92.3 | 1.2 | — |
| 000592 | -76.96 | 8.92 | — | 16.6 | 88.4 | — |
| 000596 | 26.02 | 2.14 | 1.87 | 46.8 | 6.2 | — |
| 000598 | 10.4 | 1.06 | 1.02 | 63.0 | 22.8 | — |
| 000617 | 17.78 | 0.84 | 3.56 | 57.1 | 57.2 | — |
| 000623 | 6.87 | 0.68 | — | 0.0 | 25.0 | — |
| 000625 | 27.09 | 0.93 | 0.42 | 81.5 | 2.3 | — |
| 000629 | 84.85 | 2.21 | 1.49 | 84.4 | 22.5 | — |
| 000630 | 21.56 | 2.25 | 0.32 | 76.2 | 88.8 | — |
| 000635 | -4.52 | 2.96 | — | 59.6 | 96.1 | — |
| 000636 | 142.31 | 4.63 | 1.74 | 90.8 | 95.6 | — |
| 000651 | 7.82 | 1.47 | 1.5 | 51.9 | 5.7 | — |
| 000657 | 48.63 | 12.12 | 2.22 | 81.5 | 92.0 | — |
<!-- /dataview-precompiled -->


## 实体清单（入边）

> 本段列出实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/valuations/000001-latest]] · [[10_Reference/investing/valuations/000002-latest]] · [[10_Reference/investing/valuations/000009-latest]] · [[10_Reference/investing/valuations/000021-latest]] · [[10_Reference/investing/valuations/000027-latest]]
- [[10_Reference/investing/valuations/000032-latest]] · [[10_Reference/investing/valuations/000034-latest]] · [[10_Reference/investing/valuations/000039-latest]] · [[10_Reference/investing/valuations/000050-latest]] · [[10_Reference/investing/valuations/000060-latest]]
- [[10_Reference/investing/valuations/000062-latest]] · [[10_Reference/investing/valuations/000063-latest]] · [[10_Reference/investing/valuations/000088-latest]] · [[10_Reference/investing/valuations/000100-latest]] · [[10_Reference/investing/valuations/000155-latest]]
- [[10_Reference/investing/valuations/000157-latest]] · [[10_Reference/investing/valuations/000166-latest]] · [[10_Reference/investing/valuations/000301-latest]] · [[10_Reference/investing/valuations/000333-latest]] · [[10_Reference/investing/valuations/000338-latest]]
- [[10_Reference/investing/valuations/000400-latest]] · [[10_Reference/investing/valuations/000408-latest]] · [[10_Reference/investing/valuations/000415-latest]] · [[10_Reference/investing/valuations/000423-latest]] · [[10_Reference/investing/valuations/000425-latest]]
- [[10_Reference/investing/valuations/000428-latest]] · [[10_Reference/investing/valuations/000429-latest]] · [[10_Reference/investing/valuations/000513-latest]] · [[10_Reference/investing/valuations/000519-latest]] · [[10_Reference/investing/valuations/000528-latest]]
- [[10_Reference/investing/valuations/000537-latest]] · [[10_Reference/investing/valuations/000538-latest]] · [[10_Reference/investing/valuations/000539-latest]] · [[10_Reference/investing/valuations/000559-latest]] · [[10_Reference/investing/valuations/000560-latest]]
- [[10_Reference/investing/valuations/000568-latest]] · [[10_Reference/investing/valuations/000582-latest]] · [[10_Reference/investing/valuations/000591-latest]] · [[10_Reference/investing/valuations/000592-latest]] · [[10_Reference/investing/valuations/000596-latest]]
- [[10_Reference/investing/valuations/000598-latest]] · [[10_Reference/investing/valuations/000617-latest]] · [[10_Reference/investing/valuations/000623-latest]] · [[10_Reference/investing/valuations/000625-latest]] · [[10_Reference/investing/valuations/000629-latest]]
- [[10_Reference/investing/valuations/000630-latest]] · [[10_Reference/investing/valuations/000635-latest]] · [[10_Reference/investing/valuations/000636-latest]] · [[10_Reference/investing/valuations/000651-latest]] · [[10_Reference/investing/valuations/000657-latest]]
- [[10_Reference/investing/valuations/000661-latest]] · [[10_Reference/investing/valuations/000683-latest]] · [[10_Reference/investing/valuations/000703-latest]] · [[10_Reference/investing/valuations/000708-latest]] · [[10_Reference/investing/valuations/000709-latest]]
- [[10_Reference/investing/valuations/000725-latest]] · [[10_Reference/investing/valuations/000768-latest]] · [[10_Reference/investing/valuations/000776-latest]] · [[10_Reference/investing/valuations/000792-latest]] · [[10_Reference/investing/valuations/000798-latest]]
- [[10_Reference/investing/valuations/000807-latest]] · [[10_Reference/investing/valuations/000858-latest]] · [[10_Reference/investing/valuations/000892-latest]] · [[10_Reference/investing/valuations/000895-latest]] · [[10_Reference/investing/valuations/000938-latest]]
- [[10_Reference/investing/valuations/000963-latest]] · [[10_Reference/investing/valuations/000975-latest]] · [[10_Reference/investing/valuations/000977-latest]] · [[10_Reference/investing/valuations/000988-latest]] · [[10_Reference/investing/valuations/000999-latest]]
- [[10_Reference/investing/valuations/001280-latest]] · [[10_Reference/investing/valuations/001330-latest]] · [[10_Reference/investing/valuations/001366-latest]] · [[10_Reference/investing/valuations/001391-latest]] · [[10_Reference/investing/valuations/001965-latest]]
- [[10_Reference/investing/valuations/001979-latest]] · [[10_Reference/investing/valuations/002001-latest]] · [[10_Reference/investing/valuations/002027-latest]] · [[10_Reference/investing/valuations/002028-latest]] · [[10_Reference/investing/valuations/002049-latest]]
- [[10_Reference/investing/valuations/002050-latest]] · [[10_Reference/investing/valuations/002059-latest]] · [[10_Reference/investing/valuations/002074-latest]] · [[10_Reference/investing/valuations/002084-latest]] · [[10_Reference/investing/valuations/002104-latest]]
- [[10_Reference/investing/valuations/002124-latest]] · [[10_Reference/investing/valuations/002142-latest]] · [[10_Reference/investing/valuations/002156-latest]] · [[10_Reference/investing/valuations/002179-latest]] · [[10_Reference/investing/valuations/002185-latest]]
- [[10_Reference/investing/valuations/002202-latest]] · [[10_Reference/investing/valuations/002230-latest]] · [[10_Reference/investing/valuations/002236-latest]] · [[10_Reference/investing/valuations/002241-latest]] · [[10_Reference/investing/valuations/002281-latest]]
- [[10_Reference/investing/valuations/002297-latest]] · [[10_Reference/investing/valuations/002300-latest]] · [[10_Reference/investing/valuations/002304-latest]] · [[10_Reference/investing/valuations/002311-latest]] · [[10_Reference/investing/valuations/002352-latest]]
- [[10_Reference/investing/valuations/002353-latest]] · [[10_Reference/investing/valuations/002354-latest]] · [[10_Reference/investing/valuations/002371-latest]] · [[10_Reference/investing/valuations/002384-latest]] · [[10_Reference/investing/valuations/002403-latest]]
- [[10_Reference/investing/valuations/002415-latest]] · [[10_Reference/investing/valuations/002422-latest]] · [[10_Reference/investing/valuations/002428-latest]] · [[10_Reference/investing/valuations/002460-latest]] · [[10_Reference/investing/valuations/002463-latest]]
- [[10_Reference/investing/valuations/002466-latest]] · [[10_Reference/investing/valuations/002475-latest]] · [[10_Reference/investing/valuations/002484-latest]] · [[10_Reference/investing/valuations/002493-latest]] · [[10_Reference/investing/valuations/002532-latest]]
- [[10_Reference/investing/valuations/002558-latest]] · [[10_Reference/investing/valuations/002564-latest]] · [[10_Reference/investing/valuations/002594-latest]] · [[10_Reference/investing/valuations/002600-latest]] · [[10_Reference/investing/valuations/002602-latest]]
- [[10_Reference/investing/valuations/002625-latest]] · [[10_Reference/investing/valuations/002636-latest]] · [[10_Reference/investing/valuations/002648-latest]] · [[10_Reference/investing/valuations/002679-latest]] · [[10_Reference/investing/valuations/002702-latest]]
- [[10_Reference/investing/valuations/002708-latest]] · [[10_Reference/investing/valuations/002709-latest]] · [[10_Reference/investing/valuations/002714-latest]] · [[10_Reference/investing/valuations/002736-latest]] · [[10_Reference/investing/valuations/002827-latest]]
- [[10_Reference/investing/valuations/002837-latest]] · [[10_Reference/investing/valuations/002855-latest]] · [[10_Reference/investing/valuations/002868-latest]] · [[10_Reference/investing/valuations/002909-latest]] · [[10_Reference/investing/valuations/002916-latest]]
- [[10_Reference/investing/valuations/002920-latest]] · [[10_Reference/investing/valuations/002938-latest]] · [[10_Reference/investing/valuations/003005-latest]] · [[10_Reference/investing/valuations/003040-latest]] · [[10_Reference/investing/valuations/003816-latest]]
- [[10_Reference/investing/valuations/300014-latest]] · [[10_Reference/investing/valuations/300015-latest]] · [[10_Reference/investing/valuations/300033-latest]] · [[10_Reference/investing/valuations/300058-latest]] · [[10_Reference/investing/valuations/300059-latest]]
- [[10_Reference/investing/valuations/300124-latest]] · [[10_Reference/investing/valuations/300274-latest]] · [[10_Reference/investing/valuations/300308-latest]] · [[10_Reference/investing/valuations/300316-latest]] · [[10_Reference/investing/valuations/300394-latest]]
- [[10_Reference/investing/valuations/300408-latest]] · [[10_Reference/investing/valuations/300413-latest]] · [[10_Reference/investing/valuations/300418-latest]] · [[10_Reference/investing/valuations/300433-latest]] · [[10_Reference/investing/valuations/300442-latest]]
- [[10_Reference/investing/valuations/300450-latest]] · [[10_Reference/investing/valuations/300476-latest]] · [[10_Reference/investing/valuations/300498-latest]] · [[10_Reference/investing/valuations/300502-latest]] · [[10_Reference/investing/valuations/300661-latest]]
- [[10_Reference/investing/valuations/300750-latest]] · [[10_Reference/investing/valuations/300760-latest]] · [[10_Reference/investing/valuations/300803-latest]] · [[10_Reference/investing/valuations/300866-latest]] · [[10_Reference/investing/valuations/301165-latest]]
- [[10_Reference/investing/valuations/301217-latest]] · [[10_Reference/investing/valuations/301269-latest]] · [[10_Reference/investing/valuations/301308-latest]] · [[10_Reference/investing/valuations/301511-latest]] · [[10_Reference/investing/valuations/600000-latest]]
- [[10_Reference/investing/valuations/600009-latest]] · [[10_Reference/investing/valuations/600010-latest]] · [[10_Reference/investing/valuations/600011-latest]] · [[10_Reference/investing/valuations/600015-latest]] · [[10_Reference/investing/valuations/600016-latest]]
- [[10_Reference/investing/valuations/600018-latest]] · [[10_Reference/investing/valuations/600019-latest]] · [[10_Reference/investing/valuations/600023-latest]] · [[10_Reference/investing/valuations/600025-latest]] · [[10_Reference/investing/valuations/600026-latest]]
- [[10_Reference/investing/valuations/600027-latest]] · [[10_Reference/investing/valuations/600028-latest]] · [[10_Reference/investing/valuations/600029-latest]] · [[10_Reference/investing/valuations/600030-latest]] · [[10_Reference/investing/valuations/600031-latest]]
- [[10_Reference/investing/valuations/600036-latest]] · [[10_Reference/investing/valuations/600039-latest]] · [[10_Reference/investing/valuations/600048-latest]] · [[10_Reference/investing/valuations/600050-latest]] · [[10_Reference/investing/valuations/600059-latest]]
- [[10_Reference/investing/valuations/600061-latest]] · [[10_Reference/investing/valuations/600066-latest]] · [[10_Reference/investing/valuations/600089-latest]] · [[10_Reference/investing/valuations/600104-latest]] · [[10_Reference/investing/valuations/600108-latest]]
- [[10_Reference/investing/valuations/600111-latest]] · [[10_Reference/investing/valuations/600115-latest]] · [[10_Reference/investing/valuations/600118-latest]] · [[10_Reference/investing/valuations/600121-latest]] · [[10_Reference/investing/valuations/600127-latest]]
- [[10_Reference/investing/valuations/600150-latest]] · [[10_Reference/investing/valuations/600160-latest]] · [[10_Reference/investing/valuations/600176-latest]] · [[10_Reference/investing/valuations/600183-latest]] · [[10_Reference/investing/valuations/600188-latest]]
- [[10_Reference/investing/valuations/600196-latest]] · [[10_Reference/investing/valuations/600206-latest]] · [[10_Reference/investing/valuations/600219-latest]] · [[10_Reference/investing/valuations/600221-latest]] · [[10_Reference/investing/valuations/600233-latest]]
- [[10_Reference/investing/valuations/600276-latest]] · [[10_Reference/investing/valuations/600309-latest]] · [[10_Reference/investing/valuations/600346-latest]] · [[10_Reference/investing/valuations/600354-latest]] · [[10_Reference/investing/valuations/600362-latest]]
- [[10_Reference/investing/valuations/600371-latest]] · [[10_Reference/investing/valuations/600372-latest]] · [[10_Reference/investing/valuations/600406-latest]] · [[10_Reference/investing/valuations/600415-latest]] · [[10_Reference/investing/valuations/600426-latest]]
- [[10_Reference/investing/valuations/600436-latest]] · [[10_Reference/investing/valuations/600438-latest]] · [[10_Reference/investing/valuations/600460-latest]] · [[10_Reference/investing/valuations/600482-latest]] · [[10_Reference/investing/valuations/600489-latest]]
- [[10_Reference/investing/valuations/600506-latest]] · [[10_Reference/investing/valuations/600519-latest]] · [[10_Reference/investing/valuations/600522-latest]] · [[10_Reference/investing/valuations/600540-latest]] · [[10_Reference/investing/valuations/600547-latest]]
- [[10_Reference/investing/valuations/600549-latest]] · [[10_Reference/investing/valuations/600551-latest]] · [[10_Reference/investing/valuations/600570-latest]] · [[10_Reference/investing/valuations/600584-latest]] · [[10_Reference/investing/valuations/600585-latest]]
- [[10_Reference/investing/valuations/600611-latest]] · [[10_Reference/investing/valuations/600657-latest]] · [[10_Reference/investing/valuations/600660-latest]] · [[10_Reference/investing/valuations/600674-latest]] · [[10_Reference/investing/valuations/600690-latest]]
- [[10_Reference/investing/valuations/600698-latest]] · [[10_Reference/investing/valuations/600726-latest]] · [[10_Reference/investing/valuations/600741-latest]] · [[10_Reference/investing/valuations/600760-latest]] · [[10_Reference/investing/valuations/600795-latest]]
- [[10_Reference/investing/valuations/600802-latest]] · [[10_Reference/investing/valuations/600803-latest]] · [[10_Reference/investing/valuations/600809-latest]] · [[10_Reference/investing/valuations/600828-latest]] · [[10_Reference/investing/valuations/600830-latest]]
- [[10_Reference/investing/valuations/600865-latest]] · [[10_Reference/investing/valuations/600869-latest]] · [[10_Reference/investing/valuations/600875-latest]] · [[10_Reference/investing/valuations/600886-latest]] · [[10_Reference/investing/valuations/600887-latest]]
- [[10_Reference/investing/valuations/600892-latest]] · [[10_Reference/investing/valuations/600893-latest]] · [[10_Reference/investing/valuations/600900-latest]] · [[10_Reference/investing/valuations/600905-latest]] · [[10_Reference/investing/valuations/600919-latest]]
- [[10_Reference/investing/valuations/600926-latest]] · [[10_Reference/investing/valuations/600930-latest]] · [[10_Reference/investing/valuations/600938-latest]] · [[10_Reference/investing/valuations/600941-latest]] · [[10_Reference/investing/valuations/600958-latest]]
- [[10_Reference/investing/valuations/600967-latest]] · [[10_Reference/investing/valuations/600989-latest]] · [[10_Reference/investing/valuations/600999-latest]] · [[10_Reference/investing/valuations/601006-latest]] · [[10_Reference/investing/valuations/601009-latest]]
- [[10_Reference/investing/valuations/601012-latest]] · [[10_Reference/investing/valuations/601018-latest]] · [[10_Reference/investing/valuations/601021-latest]] · [[10_Reference/investing/valuations/601058-latest]] · [[10_Reference/investing/valuations/601059-latest]]
- [[10_Reference/investing/valuations/601066-latest]] · [[10_Reference/investing/valuations/601077-latest]] · [[10_Reference/investing/valuations/601086-latest]] · [[10_Reference/investing/valuations/601088-latest]] · [[10_Reference/investing/valuations/601100-latest]]
- [[10_Reference/investing/valuations/601111-latest]] · [[10_Reference/investing/valuations/601117-latest]] · [[10_Reference/investing/valuations/601127-latest]] · [[10_Reference/investing/valuations/601136-latest]] · [[10_Reference/investing/valuations/601138-latest]]
- [[10_Reference/investing/valuations/601166-latest]] · [[10_Reference/investing/valuations/601169-latest]] · [[10_Reference/investing/valuations/601186-latest]] · [[10_Reference/investing/valuations/601208-latest]] · [[10_Reference/investing/valuations/601211-latest]]
- [[10_Reference/investing/valuations/601225-latest]] · [[10_Reference/investing/valuations/601229-latest]] · [[10_Reference/investing/valuations/601288-latest]] · [[10_Reference/investing/valuations/601318-latest]] · [[10_Reference/investing/valuations/601319-latest]]
- [[10_Reference/investing/valuations/601328-latest]] · [[10_Reference/investing/valuations/601336-latest]] · [[10_Reference/investing/valuations/601360-latest]] · [[10_Reference/investing/valuations/601377-latest]] · [[10_Reference/investing/valuations/601390-latest]]
- [[10_Reference/investing/valuations/601398-latest]] · [[10_Reference/investing/valuations/601566-latest]] · [[10_Reference/investing/valuations/601579-latest]] · [[10_Reference/investing/valuations/601600-latest]] · [[10_Reference/investing/valuations/601601-latest]]
- [[10_Reference/investing/valuations/601607-latest]] · [[10_Reference/investing/valuations/601618-latest]] · [[10_Reference/investing/valuations/601628-latest]] · [[10_Reference/investing/valuations/601633-latest]] · [[10_Reference/investing/valuations/601658-latest]]
- [[10_Reference/investing/valuations/601668-latest]] · [[10_Reference/investing/valuations/601669-latest]] · [[10_Reference/investing/valuations/601688-latest]] · [[10_Reference/investing/valuations/601689-latest]] · [[10_Reference/investing/valuations/601698-latest]]
- [[10_Reference/investing/valuations/601727-latest]] · [[10_Reference/investing/valuations/601728-latest]] · [[10_Reference/investing/valuations/601766-latest]] · [[10_Reference/investing/valuations/601788-latest]] · [[10_Reference/investing/valuations/601800-latest]]
- [[10_Reference/investing/valuations/601816-latest]] · [[10_Reference/investing/valuations/601818-latest]] · [[10_Reference/investing/valuations/601825-latest]] · [[10_Reference/investing/valuations/601838-latest]] · [[10_Reference/investing/valuations/601857-latest]]
- [[10_Reference/investing/valuations/601868-latest]] · [[10_Reference/investing/valuations/601872-latest]] · [[10_Reference/investing/valuations/601877-latest]] · [[10_Reference/investing/valuations/601878-latest]] · [[10_Reference/investing/valuations/601881-latest]]
- [[10_Reference/investing/valuations/601888-latest]] · [[10_Reference/investing/valuations/601898-latest]] · [[10_Reference/investing/valuations/601899-latest]] · [[10_Reference/investing/valuations/601901-latest]] · [[10_Reference/investing/valuations/601916-latest]]
- [[10_Reference/investing/valuations/601919-latest]] · [[10_Reference/investing/valuations/601939-latest]] · [[10_Reference/investing/valuations/601949-latest]] · [[10_Reference/investing/valuations/601985-latest]] · [[10_Reference/investing/valuations/601988-latest]]
- [[10_Reference/investing/valuations/601995-latest]] · [[10_Reference/investing/valuations/601998-latest]] · [[10_Reference/investing/valuations/603019-latest]] · [[10_Reference/investing/valuations/603083-latest]] · [[10_Reference/investing/valuations/603122-latest]]
- [[10_Reference/investing/valuations/603123-latest]] · [[10_Reference/investing/valuations/603151-latest]] · [[10_Reference/investing/valuations/603162-latest]] · [[10_Reference/investing/valuations/603207-latest]] · [[10_Reference/investing/valuations/603259-latest]]
- [[10_Reference/investing/valuations/603270-latest]] · [[10_Reference/investing/valuations/603288-latest]] · [[10_Reference/investing/valuations/603296-latest]] · [[10_Reference/investing/valuations/603390-latest]] · [[10_Reference/investing/valuations/603501-latest]]
- [[10_Reference/investing/valuations/603533-latest]] · [[10_Reference/investing/valuations/603696-latest]] · [[10_Reference/investing/valuations/603721-latest]] · [[10_Reference/investing/valuations/603799-latest]] · [[10_Reference/investing/valuations/603893-latest]]
- [[10_Reference/investing/valuations/603986-latest]] · [[10_Reference/investing/valuations/603993-latest]] · [[10_Reference/investing/valuations/605117-latest]] · [[10_Reference/investing/valuations/605398-latest]] · [[10_Reference/investing/valuations/605499-latest]]
- [[10_Reference/investing/valuations/605577-latest]] · [[10_Reference/investing/valuations/605580-latest]] · [[10_Reference/investing/valuations/688008-latest]] · [[10_Reference/investing/valuations/688009-latest]] · [[10_Reference/investing/valuations/688012-latest]]
- [[10_Reference/investing/valuations/688036-latest]] · [[10_Reference/investing/valuations/688041-latest]] · [[10_Reference/investing/valuations/688047-latest]] · [[10_Reference/investing/valuations/688048-latest]] · [[10_Reference/investing/valuations/688072-latest]]
- [[10_Reference/investing/valuations/688082-latest]] · [[10_Reference/investing/valuations/688110-latest]] · [[10_Reference/investing/valuations/688111-latest]] · [[10_Reference/investing/valuations/688126-latest]] · [[10_Reference/investing/valuations/688141-latest]]
- [[10_Reference/investing/valuations/688147-latest]] · [[10_Reference/investing/valuations/688167-latest]] · [[10_Reference/investing/valuations/688183-latest]] · [[10_Reference/investing/valuations/688223-latest]] · [[10_Reference/investing/valuations/688256-latest]]
- [[10_Reference/investing/valuations/688271-latest]] · [[10_Reference/investing/valuations/688300-latest]] · [[10_Reference/investing/valuations/688396-latest]] · [[10_Reference/investing/valuations/688409-latest]] · [[10_Reference/investing/valuations/688432-latest]]
- [[10_Reference/investing/valuations/688433-latest]] · [[10_Reference/investing/valuations/688506-latest]] · [[10_Reference/investing/valuations/688519-latest]] · [[10_Reference/investing/valuations/688521-latest]] · [[10_Reference/investing/valuations/688536-latest]]
- [[10_Reference/investing/valuations/688548-latest]] · [[10_Reference/investing/valuations/688627-latest]] · [[10_Reference/investing/valuations/688630-latest]] · [[10_Reference/investing/valuations/688766-latest]] · [[10_Reference/investing/valuations/688836-latest]]
- [[10_Reference/investing/valuations/688981-latest]]

## 关系

- belongs_to: [[10_Reference/investing/stocks/index|stocks/]]（每条估值数据所属股票）
- pairs_with: [[10_Reference/investing/metrics/index|metrics/]]（估值与财务配对看，PE = 股价 / EPS）
- consensus: [[10_Reference/investing/reports/index|reports/]]（一致预期 EPS 来自研报）
- sourced_from: [[10_Reference/investing/data-sources/index|data-sources/]]（估值数据来源）

## 新建实体

用 Templater 应用 `templates/valuation` 新建。模板 frontmatter 对应 `Valuation` + `ValuationPercentile` 字段（pe_ttm/pb/ps_ttm/pcf_ttm/dividend_yield/peg/forward_pe/consensus_eps/pe_percentile/pb_percentile）。

---

## ⚡ 快速操作

用 Templater 应用 `templates/valuation` 新建 估值 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:b6813799ccc1 -->
| 估值总数 |
|---|
| 401 |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
