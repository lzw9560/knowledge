# 股票 索引

> 个股是投研知识图谱的核心节点。对应 Pydantic 契约 `Quote` + `CompanyInfo`，覆盖 A 股/美股/港股。每只股票链接其行业、研报、财务、估值、龙虎榜、相关事件、匹配战法。

## 实体列表（Dataview 动态）

<!-- dataview-precompiled:0cd485f40a42 -->
| 代码 | 名称 | 市场 | 行业 | PE(TTM) | 市值 |
|---|---|---|---|---|---|
| 000001 | 平安银行 | A | 股份制与城商行 | 5.22 | 2267B |
| 000002 | 万科A | A | 房地产开发 | -0.41 | 309B |
| 000009 | 中国宝安 | A | 电池材料 | -258.73 | 182B |
| 000019 | 深粮控股 | A | — | — | — |
| 000021 | 深科技 | A | 半导体封测 | 45.43 | 557B |
| 000027 | 深圳能源 | A | 电力 | 12.96 | 298B |
| 000032 | 深桑达A | A | IT服务 | -71.79 | 171B |
| 000034 | 神州数码 | A | IT服务 | 40.42 | 200B |
| 000039 | 中集集团 | A | 专用设备 | -157.11 | 213B |
| 000050 | 深天马A | A | 显示器件 | -21.04 | 161B |
| 000060 | 中金岭南 | A | 铅锌 | 20.65 | 286B |
| 000062 | 深圳华强 | A | 电子元件 | 40.86 | 253B |
| 000063 | 中兴通讯 | A | 通信设备 | 47.85 | 1335B |
| 000088 | 盐田港 | A | 航运港口 | 15.8 | 143B |
| 000100 | TCL科技 | A | 显示器件 | 16.39 | 968B |
| 000155 | 川能动力 | A | 太阳能 | 24.55 | 222B |
| 000157 | 中联重科 | A | 专用设备 | 13.69 | 469B |
| 000166 | 申万宏源 | A | 证券 | 10.36 | 1021B |
| 000301 | 东方盛虹 | A | 石油加工 | 21.68 | 921B |
| 000333 | 美的集团 | A | 白色家电 | 14.8 | 5927B |
| 000338 | 潍柴动力 | A | 商用车 | 18.17 | 1354B |
| 000400 | 许继电气 | A | 电网设备 | 23.38 | 221B |
| 000408 | 藏格矿业 | A | 钾肥 | 20.57 | 1171B |
| 000415 | 渤海租赁 | A | 多元金融 | 5.74 | 241B |
| 000423 | 东阿阿胶 | A | 中药生产 | 16.98 | 303B |
| 000425 | 徐工机械 | A | 专用设备 | 15.74 | 747B |
| 000428 | 华天酒店 | A | 酒店餐饮 | -22.05 | 47.8亿 |
| 000429 | 粤高速A | A | 路桥建设 | 16.79 | 167B |
| 000505 | 京粮控股 | A | — | — | — |
| 000513 | 丽珠集团 | A | 化学制药 | 14.32 | 153B |
| 000519 | 中兵红箭 | A | 地面兵装 | 179.76 | 215B |
| 000528 | 柳工 | A | 专用设备 | 11.29 | 163B |
| 000537 | 绿发电力 | A | 太阳能 | 32.36 | 154B |
| 000538 | 云南白药 | A | 中药生产 | 17.14 | 895B |
| 000539 | 粤电力A | A | 电力 | 1232.27 | 130B |
| 000559 | 万向钱潮 | A | 汽车零部件 | 34.88 | 368B |
| 000560 | 我爱我家 | A | 房地产服务 | -136.80 | 73.8亿 |
| 000568 | 泸州老窖 | A | 白酒 | 15.55 | 1166B |
| 000582 | 北部湾港 | A | 航运港口 | 29.07 | 265B |
| 000591 | 太阳能 | A | 太阳能 | 26.24 | 167B |
| 000592 | 平潭发展 | A | 林业 | -73.25 | 143.4亿 |
| 000596 | 古井贡酒 | A | 白酒 | 25.91 | 411B |
| 000598 | 兴蓉环境 | A | 环保 | 10.39 | 213B |
| 000617 | 中油资本 | A | 多元金融 | 17.85 | 904B |
| 000623 | 吉林敖东 | A | 中药生产 | 6.9 | 217B |
| 000625 | 长安汽车 | A | 汽车整车 | 27.09 | 588B |
| 000629 | 钒钛股份 | A | 其他稀有小金属 | 84.57 | 277B |
| 000630 | 铜陵有色 | A | 铜 | 21.46 | 708B |
| 000635 | 英 力 特 | A | 化学原料 | -4.70 | 28.2亿 |
| 000636 | 风华高科 | A | 电子元件 | 140.70 | 572.37亿 |
<!-- /dataview-precompiled -->

## 关系

- belongs_to: [[10_Reference/investing/industries/index|industries/]]（每只股票属于一个证监会行业）
- tagged: [[10_Reference/investing/concepts/index|concepts/]]（每只股票可被多个概念题材打标）
- covered_by: [[10_Reference/investing/reports/index|reports/]]（机构研报覆盖）
- financials: [[10_Reference/investing/metrics/index|metrics/]]（财务周期数据）
- valued_by: [[10_Reference/investing/valuations/index|valuations/]]（估值快照）
- appears_on: [[10_Reference/investing/dragon-tiger/index|dragon-tiger/]]（龙虎榜上榜记录）
- triggers: [[10_Reference/investing/events/index|events/]]（新闻/公告/涨停事件）
- matches: [[10_Reference/investing/strategies/index|strategies/]]（匹配的战法）
- listed_in: [[10_Reference/investing/indices/index|indices/]]（宽基/行业指数成分）
- sourced_from: [[10_Reference/investing/data-sources/index|data-sources/]]（行情数据来源）

## 新建实体

用 Templater 应用 `templates/stock` 新建。模板会自动填入 YAML frontmatter（code/name/market/industry/pe_ttm/pb/market_cap 等）+ 正文骨架（基本信息/核心业务/财务速览/估值/相关研报/龙虎榜/相关事件/匹配战法）。

## 实体清单（入边）

> 本段列出该类型所有实体以建立入边链接（Dataview 表格不计入边）。

- [[10_Reference/investing/stocks/000001]]
- [[10_Reference/investing/stocks/000002]]
- [[10_Reference/investing/stocks/000009]]
- [[10_Reference/investing/stocks/000019]]
- [[10_Reference/investing/stocks/000021]]
- [[10_Reference/investing/stocks/000027]]
- [[10_Reference/investing/stocks/000032]]
- [[10_Reference/investing/stocks/000034]]
- [[10_Reference/investing/stocks/000039]]
- [[10_Reference/investing/stocks/000050]]
- [[10_Reference/investing/stocks/000060]]
- [[10_Reference/investing/stocks/000062]]
- [[10_Reference/investing/stocks/000063]]
- [[10_Reference/investing/stocks/000088]]
- [[10_Reference/investing/stocks/000100]]
- [[10_Reference/investing/stocks/000155]]
- [[10_Reference/investing/stocks/000157]]
- [[10_Reference/investing/stocks/000166]]
- [[10_Reference/investing/stocks/000301]]
- [[10_Reference/investing/stocks/000333]]
- [[10_Reference/investing/stocks/000338]]
- [[10_Reference/investing/stocks/000400]]
- [[10_Reference/investing/stocks/000408]]
- [[10_Reference/investing/stocks/000415]]
- [[10_Reference/investing/stocks/000423]]
- [[10_Reference/investing/stocks/000425]]
- [[10_Reference/investing/stocks/000428]]
- [[10_Reference/investing/stocks/000429]]
- [[10_Reference/investing/stocks/000505]]
- [[10_Reference/investing/stocks/000513]]
- [[10_Reference/investing/stocks/000519]]
- [[10_Reference/investing/stocks/000528]]
- [[10_Reference/investing/stocks/000537]]
- [[10_Reference/investing/stocks/000538]]
- [[10_Reference/investing/stocks/000539]]
- [[10_Reference/investing/stocks/000559]]
- [[10_Reference/investing/stocks/000560]]
- [[10_Reference/investing/stocks/000568]]
- [[10_Reference/investing/stocks/000582]]
- [[10_Reference/investing/stocks/000591]]
- [[10_Reference/investing/stocks/000592]]
- [[10_Reference/investing/stocks/000596]]
- [[10_Reference/investing/stocks/000598]]
- [[10_Reference/investing/stocks/000617]]
- [[10_Reference/investing/stocks/000623]]
- [[10_Reference/investing/stocks/000625]]
- [[10_Reference/investing/stocks/000629]]
- [[10_Reference/investing/stocks/000630]]
- [[10_Reference/investing/stocks/000635]]
- [[10_Reference/investing/stocks/000636]]
- [[10_Reference/investing/stocks/000651]]
- [[10_Reference/investing/stocks/000657]]
- [[10_Reference/investing/stocks/000661]]
- [[10_Reference/investing/stocks/000683]]
- [[10_Reference/investing/stocks/000703]]
- [[10_Reference/investing/stocks/000708]]
- [[10_Reference/investing/stocks/000709]]
- [[10_Reference/investing/stocks/000725]]
- [[10_Reference/investing/stocks/000768]]
- [[10_Reference/investing/stocks/000776]]
- [[10_Reference/investing/stocks/000792]]
- [[10_Reference/investing/stocks/000798]]
- [[10_Reference/investing/stocks/000807]]
- [[10_Reference/investing/stocks/000858]]
- [[10_Reference/investing/stocks/000892]]
- [[10_Reference/investing/stocks/000895]]
- [[10_Reference/investing/stocks/000938]]
- [[10_Reference/investing/stocks/000963]]
- [[10_Reference/investing/stocks/000975]]
- [[10_Reference/investing/stocks/000977]]
- [[10_Reference/investing/stocks/000988]]
- [[10_Reference/investing/stocks/000999]]
- [[10_Reference/investing/stocks/001280]]
- [[10_Reference/investing/stocks/001330]]
- [[10_Reference/investing/stocks/001366]]
- [[10_Reference/investing/stocks/001391]]
- [[10_Reference/investing/stocks/001965]]
- [[10_Reference/investing/stocks/001979]]
- [[10_Reference/investing/stocks/002001]]
- [[10_Reference/investing/stocks/002027]]
- [[10_Reference/investing/stocks/002028]]
- [[10_Reference/investing/stocks/002049]]
- [[10_Reference/investing/stocks/002050]]
- [[10_Reference/investing/stocks/002059]]
- [[10_Reference/investing/stocks/002074]]
- [[10_Reference/investing/stocks/002084]]
- [[10_Reference/investing/stocks/002104]]
- [[10_Reference/investing/stocks/002124]]
- [[10_Reference/investing/stocks/002142]]
- [[10_Reference/investing/stocks/002156]]
- [[10_Reference/investing/stocks/002172]]
- [[10_Reference/investing/stocks/002179]]
- [[10_Reference/investing/stocks/002185]]
- [[10_Reference/investing/stocks/002202]]
- [[10_Reference/investing/stocks/002230]]
- [[10_Reference/investing/stocks/002236]]
- [[10_Reference/investing/stocks/002241]]
- [[10_Reference/investing/stocks/002281]]
- [[10_Reference/investing/stocks/002297]]
- [[10_Reference/investing/stocks/002300]]
- [[10_Reference/investing/stocks/002304]]
- [[10_Reference/investing/stocks/002311]]
- [[10_Reference/investing/stocks/002352]]
- [[10_Reference/investing/stocks/002353]]
- [[10_Reference/investing/stocks/002354]]
- [[10_Reference/investing/stocks/002371]]
- [[10_Reference/investing/stocks/002384]]
- [[10_Reference/investing/stocks/002403]]
- [[10_Reference/investing/stocks/002415]]
- [[10_Reference/investing/stocks/002422]]
- [[10_Reference/investing/stocks/002428]]
- [[10_Reference/investing/stocks/002460]]
- [[10_Reference/investing/stocks/002463]]
- [[10_Reference/investing/stocks/002466]]
- [[10_Reference/investing/stocks/002475]]
- [[10_Reference/investing/stocks/002484]]
- [[10_Reference/investing/stocks/002493]]
- [[10_Reference/investing/stocks/002532]]
- [[10_Reference/investing/stocks/002558]]
- [[10_Reference/investing/stocks/002564]]
- [[10_Reference/investing/stocks/002594]]
- [[10_Reference/investing/stocks/002600]]
- [[10_Reference/investing/stocks/002602]]
- [[10_Reference/investing/stocks/002625]]
- [[10_Reference/investing/stocks/002636]]
- [[10_Reference/investing/stocks/002648]]
- [[10_Reference/investing/stocks/002679]]
- [[10_Reference/investing/stocks/002696]]
- [[10_Reference/investing/stocks/002702]]
- [[10_Reference/investing/stocks/002708]]
- [[10_Reference/investing/stocks/002709]]
- [[10_Reference/investing/stocks/002714]]
- [[10_Reference/investing/stocks/002736]]
- [[10_Reference/investing/stocks/002827]]
- [[10_Reference/investing/stocks/002837]]
- [[10_Reference/investing/stocks/002855]]
- [[10_Reference/investing/stocks/002868]]
- [[10_Reference/investing/stocks/002909]]
- [[10_Reference/investing/stocks/002916]]
- [[10_Reference/investing/stocks/002920]]
- [[10_Reference/investing/stocks/002938]]
- [[10_Reference/investing/stocks/003005]]
- [[10_Reference/investing/stocks/003040]]
- [[10_Reference/investing/stocks/003816]]
- [[10_Reference/investing/stocks/300014]]
- [[10_Reference/investing/stocks/300015]]
- [[10_Reference/investing/stocks/300033]]
- [[10_Reference/investing/stocks/300058]]
- [[10_Reference/investing/stocks/300059]]
- [[10_Reference/investing/stocks/300124]]
- [[10_Reference/investing/stocks/300274]]
- [[10_Reference/investing/stocks/300308]]
- [[10_Reference/investing/stocks/300316]]
- [[10_Reference/investing/stocks/300394]]
- [[10_Reference/investing/stocks/300408]]
- [[10_Reference/investing/stocks/300413]]
- [[10_Reference/investing/stocks/300418]]
- [[10_Reference/investing/stocks/300433]]
- [[10_Reference/investing/stocks/300442]]
- [[10_Reference/investing/stocks/300450]]
- [[10_Reference/investing/stocks/300476]]
- [[10_Reference/investing/stocks/300498]]
- [[10_Reference/investing/stocks/300502]]
- [[10_Reference/investing/stocks/300661]]
- [[10_Reference/investing/stocks/300750]]
- [[10_Reference/investing/stocks/300760]]
- [[10_Reference/investing/stocks/300803]]
- [[10_Reference/investing/stocks/300866]]
- [[10_Reference/investing/stocks/301165]]
- [[10_Reference/investing/stocks/301217]]
- [[10_Reference/investing/stocks/301269]]
- [[10_Reference/investing/stocks/301308]]
- [[10_Reference/investing/stocks/301511]]
- [[10_Reference/investing/stocks/600000]]
- [[10_Reference/investing/stocks/600009]]
- [[10_Reference/investing/stocks/600010]]
- [[10_Reference/investing/stocks/600011]]
- [[10_Reference/investing/stocks/600015]]
- [[10_Reference/investing/stocks/600016]]
- [[10_Reference/investing/stocks/600018]]
- [[10_Reference/investing/stocks/600019]]
- [[10_Reference/investing/stocks/600023]]
- [[10_Reference/investing/stocks/600025]]
- [[10_Reference/investing/stocks/600026]]
- [[10_Reference/investing/stocks/600027]]
- [[10_Reference/investing/stocks/600028]]
- [[10_Reference/investing/stocks/600029]]
- [[10_Reference/investing/stocks/600030]]
- [[10_Reference/investing/stocks/600031]]
- [[10_Reference/investing/stocks/600036]]
- [[10_Reference/investing/stocks/600039]]
- [[10_Reference/investing/stocks/600048]]
- [[10_Reference/investing/stocks/600050]]
- [[10_Reference/investing/stocks/600059]]
- [[10_Reference/investing/stocks/600061]]
- [[10_Reference/investing/stocks/600066]]
- [[10_Reference/investing/stocks/600089]]
- [[10_Reference/investing/stocks/600104]]
- [[10_Reference/investing/stocks/600108]]
- [[10_Reference/investing/stocks/600111]]
- [[10_Reference/investing/stocks/600115]]
- [[10_Reference/investing/stocks/600118]]
- [[10_Reference/investing/stocks/600121]]
- [[10_Reference/investing/stocks/600127]]
- [[10_Reference/investing/stocks/600150]]
- [[10_Reference/investing/stocks/600160]]
- [[10_Reference/investing/stocks/600176]]
- [[10_Reference/investing/stocks/600183]]
- [[10_Reference/investing/stocks/600188]]
- [[10_Reference/investing/stocks/600196]]
- [[10_Reference/investing/stocks/600206]]
- [[10_Reference/investing/stocks/600219]]
- [[10_Reference/investing/stocks/600221]]
- [[10_Reference/investing/stocks/600233]]
- [[10_Reference/investing/stocks/600276]]
- [[10_Reference/investing/stocks/600309]]
- [[10_Reference/investing/stocks/600313]]
- [[10_Reference/investing/stocks/600346]]
- [[10_Reference/investing/stocks/600354]]
- [[10_Reference/investing/stocks/600362]]
- [[10_Reference/investing/stocks/600371]]
- [[10_Reference/investing/stocks/600372]]
- [[10_Reference/investing/stocks/600406]]
- [[10_Reference/investing/stocks/600415]]
- [[10_Reference/investing/stocks/600426]]
- [[10_Reference/investing/stocks/600436]]
- [[10_Reference/investing/stocks/600438]]
- [[10_Reference/investing/stocks/600460]]
- [[10_Reference/investing/stocks/600482]]
- [[10_Reference/investing/stocks/600489]]
- [[10_Reference/investing/stocks/600506]]
- [[10_Reference/investing/stocks/600519]]
- [[10_Reference/investing/stocks/600522]]
- [[10_Reference/investing/stocks/600540]]
- [[10_Reference/investing/stocks/600547]]
- [[10_Reference/investing/stocks/600549]]
- [[10_Reference/investing/stocks/600551]]
- [[10_Reference/investing/stocks/600570]]
- [[10_Reference/investing/stocks/600584]]
- [[10_Reference/investing/stocks/600585]]
- [[10_Reference/investing/stocks/600611]]
- [[10_Reference/investing/stocks/600657]]
- [[10_Reference/investing/stocks/600660]]
- [[10_Reference/investing/stocks/600674]]
- [[10_Reference/investing/stocks/600690]]
- [[10_Reference/investing/stocks/600693]]
- [[10_Reference/investing/stocks/600698]]
- [[10_Reference/investing/stocks/600726]]
- [[10_Reference/investing/stocks/600741]]
- [[10_Reference/investing/stocks/600760]]
- [[10_Reference/investing/stocks/600795]]
- [[10_Reference/investing/stocks/600802]]
- [[10_Reference/investing/stocks/600803]]
- [[10_Reference/investing/stocks/600809]]
- [[10_Reference/investing/stocks/600828]]
- [[10_Reference/investing/stocks/600830]]
- [[10_Reference/investing/stocks/600865]]
- [[10_Reference/investing/stocks/600869]]
- [[10_Reference/investing/stocks/600875]]
- [[10_Reference/investing/stocks/600886]]
- [[10_Reference/investing/stocks/600887]]
- [[10_Reference/investing/stocks/600892]]
- [[10_Reference/investing/stocks/600893]]
- [[10_Reference/investing/stocks/600900]]
- [[10_Reference/investing/stocks/600905]]
- [[10_Reference/investing/stocks/600919]]
- [[10_Reference/investing/stocks/600926]]
- [[10_Reference/investing/stocks/600930]]
- [[10_Reference/investing/stocks/600938]]
- [[10_Reference/investing/stocks/600941]]
- [[10_Reference/investing/stocks/600958]]
- [[10_Reference/investing/stocks/600967]]
- [[10_Reference/investing/stocks/600989]]
- [[10_Reference/investing/stocks/600999]]
- [[10_Reference/investing/stocks/601006]]
- [[10_Reference/investing/stocks/601009]]
- [[10_Reference/investing/stocks/601012]]
- [[10_Reference/investing/stocks/601018]]
- [[10_Reference/investing/stocks/601021]]
- [[10_Reference/investing/stocks/601058]]
- [[10_Reference/investing/stocks/601059]]
- [[10_Reference/investing/stocks/601066]]
- [[10_Reference/investing/stocks/601077]]
- [[10_Reference/investing/stocks/601086]]
- [[10_Reference/investing/stocks/601088]]
- [[10_Reference/investing/stocks/601100]]
- [[10_Reference/investing/stocks/601111]]
- [[10_Reference/investing/stocks/601117]]
- [[10_Reference/investing/stocks/601127]]
- [[10_Reference/investing/stocks/601136]]
- [[10_Reference/investing/stocks/601138]]
- [[10_Reference/investing/stocks/601166]]
- [[10_Reference/investing/stocks/601169]]
- [[10_Reference/investing/stocks/601186]]
- [[10_Reference/investing/stocks/601208]]
- [[10_Reference/investing/stocks/601211]]
- [[10_Reference/investing/stocks/601225]]
- [[10_Reference/investing/stocks/601229]]
- [[10_Reference/investing/stocks/601288]]
- [[10_Reference/investing/stocks/601318]]
- [[10_Reference/investing/stocks/601319]]
- [[10_Reference/investing/stocks/601328]]
- [[10_Reference/investing/stocks/601336]]
- [[10_Reference/investing/stocks/601360]]
- [[10_Reference/investing/stocks/601377]]
- [[10_Reference/investing/stocks/601390]]
- [[10_Reference/investing/stocks/601398]]
- [[10_Reference/investing/stocks/601566]]
- [[10_Reference/investing/stocks/601579]]
- [[10_Reference/investing/stocks/601600]]
- [[10_Reference/investing/stocks/601601]]
- [[10_Reference/investing/stocks/601607]]
- [[10_Reference/investing/stocks/601618]]
- [[10_Reference/investing/stocks/601628]]
- [[10_Reference/investing/stocks/601633]]
- [[10_Reference/investing/stocks/601658]]
- [[10_Reference/investing/stocks/601668]]
- [[10_Reference/investing/stocks/601669]]
- [[10_Reference/investing/stocks/601688]]
- [[10_Reference/investing/stocks/601689]]
- [[10_Reference/investing/stocks/601698]]
- [[10_Reference/investing/stocks/601727]]
- [[10_Reference/investing/stocks/601728]]
- [[10_Reference/investing/stocks/601766]]
- [[10_Reference/investing/stocks/601788]]
- [[10_Reference/investing/stocks/601800]]
- [[10_Reference/investing/stocks/601816]]
- [[10_Reference/investing/stocks/601818]]
- [[10_Reference/investing/stocks/601825]]
- [[10_Reference/investing/stocks/601838]]
- [[10_Reference/investing/stocks/601857]]
- [[10_Reference/investing/stocks/601868]]
- [[10_Reference/investing/stocks/601872]]
- [[10_Reference/investing/stocks/601877]]
- [[10_Reference/investing/stocks/601878]]
- [[10_Reference/investing/stocks/601881]]
- [[10_Reference/investing/stocks/601888]]
- [[10_Reference/investing/stocks/601898]]
- [[10_Reference/investing/stocks/601899]]
- [[10_Reference/investing/stocks/601901]]
- [[10_Reference/investing/stocks/601916]]
- [[10_Reference/investing/stocks/601919]]
- [[10_Reference/investing/stocks/601939]]
- [[10_Reference/investing/stocks/601949]]
- [[10_Reference/investing/stocks/601985]]
- [[10_Reference/investing/stocks/601988]]
- [[10_Reference/investing/stocks/601995]]
- [[10_Reference/investing/stocks/601998]]
- [[10_Reference/investing/stocks/603019]]
- [[10_Reference/investing/stocks/603083]]
- [[10_Reference/investing/stocks/603118]]
- [[10_Reference/investing/stocks/603122]]
- [[10_Reference/investing/stocks/603123]]
- [[10_Reference/investing/stocks/603151]]
- [[10_Reference/investing/stocks/603162]]
- [[10_Reference/investing/stocks/603207]]
- [[10_Reference/investing/stocks/603221]]
- [[10_Reference/investing/stocks/603259]]
- [[10_Reference/investing/stocks/603270]]
- [[10_Reference/investing/stocks/603288]]
- [[10_Reference/investing/stocks/603296]]
- [[10_Reference/investing/stocks/603390]]
- [[10_Reference/investing/stocks/603501]]
- [[10_Reference/investing/stocks/603533]]
- [[10_Reference/investing/stocks/603626]]
- [[10_Reference/investing/stocks/603696]]
- [[10_Reference/investing/stocks/603721]]
- [[10_Reference/investing/stocks/603799]]
- [[10_Reference/investing/stocks/603893]]
- [[10_Reference/investing/stocks/603986]]
- [[10_Reference/investing/stocks/603993]]
- [[10_Reference/investing/stocks/605117]]
- [[10_Reference/investing/stocks/605188]]
- [[10_Reference/investing/stocks/605398]]
- [[10_Reference/investing/stocks/605499]]
- [[10_Reference/investing/stocks/605577]]
- [[10_Reference/investing/stocks/605580]]
- [[10_Reference/investing/stocks/688008]]
- [[10_Reference/investing/stocks/688009]]
- [[10_Reference/investing/stocks/688012]]
- [[10_Reference/investing/stocks/688036]]
- [[10_Reference/investing/stocks/688041]]
- [[10_Reference/investing/stocks/688047]]
- [[10_Reference/investing/stocks/688048]]
- [[10_Reference/investing/stocks/688072]]
- [[10_Reference/investing/stocks/688082]]
- [[10_Reference/investing/stocks/688110]]
- [[10_Reference/investing/stocks/688111]]
- [[10_Reference/investing/stocks/688126]]
- [[10_Reference/investing/stocks/688141]]
- [[10_Reference/investing/stocks/688147]]
- [[10_Reference/investing/stocks/688167]]
- [[10_Reference/investing/stocks/688183]]
- [[10_Reference/investing/stocks/688223]]
- [[10_Reference/investing/stocks/688256]]
- [[10_Reference/investing/stocks/688271]]
- [[10_Reference/investing/stocks/688300]]
- [[10_Reference/investing/stocks/688396]]
- [[10_Reference/investing/stocks/688409]]
- [[10_Reference/investing/stocks/688432]]
- [[10_Reference/investing/stocks/688433]]
- [[10_Reference/investing/stocks/688506]]
- [[10_Reference/investing/stocks/688519]]
- [[10_Reference/investing/stocks/688521]]
- [[10_Reference/investing/stocks/688536]]
- [[10_Reference/investing/stocks/688548]]
- [[10_Reference/investing/stocks/688627]]
- [[10_Reference/investing/stocks/688630]]
- [[10_Reference/investing/stocks/688766]]
- [[10_Reference/investing/stocks/688836]]
- [[10_Reference/investing/stocks/688981]]

---

## ⚡ 快速操作

用 Templater 应用 `templates/stock` 新建 股票 实体。
模板会自动填入 YAML frontmatter + 正文骨架（callout + emoji + Dataview 查询）。

## 📊 Dataview 实时统计

<!-- dataview-precompiled:f021248313f1 -->
| 股票总数 |
|---|
| 411 |
<!-- /dataview-precompiled -->

## 🔗 相关子区

- [[10_Reference/investing/MOC|投研 MOC]] — 知识图谱入口
- [[10_Reference/investing/reviews/index|审查报告]] — ReAct Agent 体检
- [[10_Reference/investing/inbox/index|待审区]] — LLM 抽取实体暂存
