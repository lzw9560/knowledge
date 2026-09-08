# Vibe-Research Obsidian Vault 使用指南

> 面向"vault 已搭好但不知道怎么用"的用户。本指南假设你已经能跟着 knowledge/README.md 用 Obsidian 打开 `knowledge/` 文件夹，但想真正把它跑起来——装插件、新建实体、做查询、看图谱、接 AI。
>
> 配套文档：obsidian-mcp-setup.md 讲 MCP 连接的详细步骤。本文只讲 vault 内的操作。

---

## 1. 这个 vault 是什么

**一句话**：Vibe-Research 的语义知识层，把代码里的实体、spec 决策、战法、数据源链接成可导航的知识图谱。

Vibe-Research 项目分两层：

| 层 | 位置 | 职责 |
|---|---|---|
| **执行层（代码）** | `backend/` | 数据采集/加工/存储/战法 match——管"数据怎么流" |
| **认知层（本 vault）** | `knowledge/` | 实体关系导航、研报笔记、投研知识沉淀——管"知识怎么连" |

代码层用 Pydantic 模型定义数据结构（Quote/Valuation/Financials/Report…），跑管线产出数字；本 vault 用 Markdown 笔记 + `[[]]` 双链把这些数字和决策织成网。一只股票笔记会链接到它的行业、被哪些研报覆盖、触发哪张战法、数据从哪个源来——形成可回溯的投研上下文。

**核心定位**：本 vault 不复制代码逻辑，只做知识表征。模板的 frontmatter 字段名对应 Pydantic 模型字段，代码改了模型字段，来这里改对应模板的 frontmatter 即可保持一致。

---

## 2. 打开 vault

### 2.1 安装 Obsidian

到 obsidian.md 下载桌面端（Windows/macOS/Linux 均免费），安装。

### 2.2 打开 vault

1. 启动 Obsidian → 点 **Open vault as folder**（不是 "Create new vault"）。
2. 选 `/Users/lizhiwei/project/code/stock/Vibe-Research/knowledge/` 文件夹。
3. 弹出"是否信任此文件夹作者" → **Trust author and enable plugins**。

> `.obsidian/` 配置目录会自动生成，已在 `.gitignore` 中忽略个人状态，不会污染仓库。

### 2.3 首次设置

打开后默认会有核心插件开着（Files、Search、Graph、Tags、Backlinks、Daily notes）。检查一遍：

- **设置 → Community plugins**：如果是第一次用社区插件，需要先点 **Turn on community plugins**（接受风险提示）。
- **设置 → Editor → Default view for new tabs**：建议设为 **Editing view**，因为阶段 0 主要是写笔记而非读。
- 左下角齿轮 → **About → Interface language**：可选简体中文。

---

## 3. 推荐插件清单

### 3.1 必装 + 推荐表

| 插件 | 类型 | 必装/推荐 | 用途 |
|---|---|---|---|
| Dataview | 社区 | 必装 | DQL 查询实体（如"查白酒行业所有股票"） |
| Templater | 社区 | 必装 | 用模板新建实体（stocks/industries/...） |
| Smart Connections | 社区 | 推荐 | 语义检索"找和茅台相似的公司" |
| Copilot for Obsidian | 社区 | 推荐 | 对话式问答 vault 内容 |
| Graph Analysis | 社区 | 推荐 | 共引分析/链接预测/社区发现 |
| Canvas | 核心 | 推荐 | 画产业链/竞争格局白板 |
| Excalidraw | 社区 | 可选 | 手绘风格关系图 |

### 3.2 安装步骤（通用）

社区插件安装流程：

1. 设置 → **Community plugins** → **Browse**（浏览）。
2. 在搜索框输入插件名。
3. 点插件条目 → **Install** → 安装完点 **Enable**。
4. 回到插件列表，点齿轮图标进入该插件的设置。

核心插件（Canvas）无需安装，在 **Settings → Core plugins** 里打开开关即可。

### 3.3 各插件配置要点

**Dataview（必装）**
- 设置 → Dataview → 开启 **Enable JavaScript Queries**（如需 JS 查询）和 **Enable Inline Queries**（行内查询）。
- 其它默认即可。装好后所有 ```dataview 代码块会自动渲染成表格/列表。
- 阶段 0 不需要额外配置，开箱即用。

**Templater（必装）**
- 设置 → Templater → **Template folder location** 填 `templates`。
- **Trigger Templater on new file creation**：开启（这样在实体文件夹右键新建笔记时能自动套模板）。
- **Folder Templates**：可按文件夹映射模板，例如 `stocks/` → `templates/stock.md`，但阶段 0 用命令面板手动套更直观。

**Smart Connections（推荐）**
- 装上后第一次启用会自动为所有笔记建索引（vault 不大时很快）。
- 设置 → Smart Connections → **Model**：默认用 OpenAI 的 embedding。**待验证**：阶段 0 是否支持纯本地模型（如 transformers.js）。不配置 API key 时插件不报错，只是不工作。
- 右侧栏会出现 Smart Connections 面板，打开任意笔记时自动列出相似笔记。

**Copilot for Obsidian（推荐）**
- 需要 OpenAI API key 或兼容端点。设置 → Copilot → 填 key。
- `Ctrl/Cmd+P` → "Copilot" → 打开聊天面板，可以问"这个 vault 里讲白酒的笔记有哪些"。
- 不配 key 时静默不工作。

**Graph Analysis（推荐）**
- 依赖 Obsidian 图谱视图的双链数据。装上后命令面板 → "Graph Analysis" 可跑链接预测、社区发现。
- 阶段 0 笔记少时价值有限，等导入一批龙头股后再用。

**Canvas（核心，推荐）**
- 核心插件，Settings → Core plugins → 开启 **Canvas**。
- 命令面板 → "Create new canvas" → 拖入笔记节点 + 连线，画产业链/竞争格局白板。
- 适合画"茅台→上游高粱/包装→下游经销商→终端零售"这种链路。

**Excalidraw（可选）**
- 社区插件，安装同上。装上后在命令面板搜 "Excalidraw" 新建画板。
- 手绘风格，适合做"情绪+资金+题材"三角图这种非结构化表达。

---

## 4. 目录结构说明

```
knowledge/
├── MOC.md                  # Map of Content，vault 入口
├── README.md               # vault 自带说明
├── stocks/                 # 股票实体（对应 Quote + CompanyInfo）
├── industries/            # 行业板块（对应 IndustrySector）
├── concepts/               # 概念题材板块（对应 ConceptBlock + Sector）
├── indices/                # 指数（沪深300/中证500等）
├── reports/                # 机构研报（对应 Report）
├── analysts/               # 研报作者（对应 Report.researcher）
├── metrics/                # 财务指标（对应 Financials + FinancialPeriod）
├── valuations/             # 估值快照（对应 Valuation + ValuationPercentile）
├── dragon-tiger/           # 龙虎榜（对应 Seat + BillboardDetail + DragonTiger）
├── events/                 # 事件（对应 News + Announcement + ZTPoolItem）
├── strategies/             # 战法卡（12 张，已从 backend/strategies/cards/ 导入）
├── specs/                  # 项目决策（SDD spec 实体）
├── data-sources/           # 数据源（15+ 外部源）
├── templates/              # Templater 模板（13 个：stock/industry/concept/index/report/analyst/metric/valuation/dragon-tiger/event/strategy/spec/data-source）
└── .obsidian/              # Obsidian 配置（已 gitignore）
```

每个实体文件夹下都有一个 `index.md`，是该实体类的 Dataview 动态列表入口。从 `MOC.md` 开始导航即可触达任意实体类。

---

## 5. 核心操作指南

### 5.1 新建一个股票实体

以创建"贵州茅台（600519）"为例。

**步骤 1：在 stocks/ 文件夹新建笔记**

左侧文件树 → 右键 `stocks/` 文件夹 → New note → 命名 `600519`（用股票代码做文件名，和模板 frontmatter 的 `code` 字段一致）。

**步骤 2：用 Templater 应用 stock.md 模板**

命令面板 `Ctrl/Cmd+P` → 输入 "Templater: Open insert template modal" → 选 `stock`。模板内容会插入当前笔记，`<% tp.date.now("YYYY-MM-DD") %>` 自动替换成今天日期。

> 如果第 3.3 节开了 "Trigger Templater on new file creation"，新建笔记时会自动弹出模板选择框，省一步。

**步骤 3：填 frontmatter**

模板头部是 YAML frontmatter，填实：

```yaml
---
type: stock
code: 600519
name: 贵州茅台
market: A
industry: 食品饮料
concept: [白酒, 高端白酒, 价值白马]
list_date: 2001-08-27
st: false
pe_ttm: 25.3
pb: 8.1
market_cap: 20000
created: 2026-09-06
---
```

**步骤 4：在正文用 `[[]]` 链接到行业、概念、研报**

在"核心业务"章节下写：

```markdown
# 核心业务

贵州茅台是 食品饮料 龙头，主营高端酱香型白酒。
品牌矩阵：飞天茅台为主，白酒 题材核心标的。
被多份研报覆盖，详见"相关研报"章节自动渲染。
```

保存后，"基本信息/财务速览/估值/相关研报/龙虎榜/相关事件/匹配战法"几个 Dataview 表会自动渲染（前提是那些实体笔记已存在且有对应 frontmatter）。

### 5.2 用 Dataview 查询实体

#### 基础语法

```dataview
TABLE 字段1 AS "列名1", 字段2 AS "列名2"
FROM "文件夹"
WHERE 条件
SORT 字段 ASC/DESC
LIMIT n
```

- `FROM "stocks"` 表示从 `stocks/` 文件夹取笔记。
- `WHERE type = "stock"` 按 frontmatter 字段过滤。
- `TABLE` 渲染表格，`LIST` 渲染列表，`TASK` 渲染待办。

#### 三个实用查询示例

**a. 查某行业所有股票**

```dataview
TABLE code AS "代码", name AS "名称", market_cap AS "市值"
FROM "stocks"
WHERE type = "stock" AND industry = "食品饮料"
SORT market_cap DESC
```

**b. 查某分析师所有研报**

```dataview
TABLE title AS "标题", code AS "标的", publish_date AS "日期", rating_change AS "评级", target_price AS "目标价"
FROM "reports"
WHERE type = "report" AND researcher = "张三"
SORT publish_date DESC
```

**c. 查没有填 industry 属性的股票（找断链）**

```dataview
TABLE code AS "代码", name AS "名称"
FROM "stocks"
WHERE type = "stock" AND !industry
SORT code ASC
```

`!industry` 表示该字段为空或不存在——这是找"还没链接到行业"的断链笔记，定期跑一遍保持图谱完整。

#### 查询放哪

Dataview 查询可以放在任意 `.md` 笔记里。建议放法：

- **实体类入口 `index.md`**：每个文件夹的 `index.md` 放该类的总览查询。
- **`MOC.md`**：放跨实体类的统计查询（已内置战法卡统计、spec 统计）。
- **临时查询笔记**：新建一个 `scratch-查询.md`，写完看完就删。

> Dataview 是只读的，查询结果不会写入文件——每次打开笔记实时渲染。

### 5.3 看图谱

#### 全局图谱视图

快捷键 `Ctrl/Cmd+G` 打开图谱视图（或左侧栏图标）。会看到所有笔记作为节点、双链作为边的网络。

**筛选技巧**：

- 顶部搜索框：输入 `path:stocks/` 只看 stocks 文件夹的节点。
- **Filters** 区：加规则 `type: stock` 按 frontmatter 字段过滤。
- **Groups** 区：按 `type` 字段分组，每组一种颜色。建议配：
  - `type: stock` → 蓝色
  - `type: industry` → 绿色
  - `type: report` → 橙色
  - `type: strategy` → 紫色
  - `type: spec` → 红色

#### 局部图谱（当前笔记的上下游）

在任意笔记打开状态下，右侧栏点 **Backlinks** 图标旁的 **Open local graph**（或命令面板 → "Graph: Open local graph"）。显示当前笔记的入链/出链节点。

用底部滑块调"层级深度"：1 层只看直连，2-3 层看二度/三度关联，对追"这只股票→行业→同行业其它股→它们的研报"链路很有用。

### 5.4 用 `[[]]` 建立关系

#### 基本语法

```markdown
600519
```

链接到 `stocks/600519.md`。若笔记不存在，Obsidian 高亮提示，点击即创建。

#### 别名语法

```markdown
茅台
```

显示为"茅台"，实际指向 600519 笔记。在正文里写"茅台今日涨停"更自然。

#### 嵌入语法

```markdown
!600519
```

把 600519 笔记内容嵌入当前笔记——适合在战法卡里嵌入它匹配的股票的财务摘要。

#### 文件夹链接

```markdown
stocks/
```

指向 `stocks/index.md`，作为该实体类的入口。

---

## 6. MOC 使用

`MOC.md`（Map of Content）是 vault 的入口，位于根目录。打开它就能看到全貌。

### 6.1 MOC 的结构

MOC.md 当前包含：

1. **顶部说明**：一段话讲 vault 定位。
2. **实体类导航表**：13 行，每行一个实体类（股票/行业/概念/指数/研报/分析师/财务指标/估值/龙虎榜/事件/战法/项目决策/数据源），给文件夹链接 + 说明 + 当前数量。
3. **战法卡统计**：一个 Dataview 查询，列出所有战法卡。
4. **项目决策统计**：一个 Dataview 查询，列出所有 spec 实体。
5. **使用说明**：新建实体/链接/查询/图谱四节速查。
6. **与项目代码的关系**：层级对照表。

### 6.2 从 MOC 导航到任意实体类

1. 打开 `MOC.md`。
2. 点导航表里的文件夹链接（如 ``）→ 跳到该文件夹的 `index.md`。
3. `index.md` 里是 Dataview 查询，列出该类所有实体。
4. 点列表里任意一行 → 进入该实体笔记。

这就是从"全景"到"单个股票"的三跳路径：MOC → 实体类入口 → 具体实体。

---

## 7. 战法卡的使用

`strategies/` 文件夹下有 12 张战法卡（已从 `backend/strategies/cards/` 导入）：首板、接力、龙头发力、尾盘偷袭、低吸、N 字反击、平台突破、弱转强、反包、破板回封、风暴反转、形态反转。

### 7.1 战法卡的结构

每张战法卡是 `type: strategy` 的笔记，frontmatter 含战法名/edge 家族等字段。正文是战法逻辑描述。

### 7.2 用 Dataview 查"某战法匹配的股票"

在战法卡笔记里追加查询（或临时查询笔记里跑）：

```dataview
TABLE code AS "代码", name AS "名称", industry AS "行业"
FROM "stocks"
WHERE type = "stock" AND contains(strategies, this.name)
SORT market_cap DESC
```

> 前提：股票笔记的 frontmatter 里维护一个 `strategies` 列表字段（如 `[首板, 弱转强]`）。阶段 0 这个字段需要手动填或后续 LLM 推断填充——模板的"匹配战法"章节已留好位置。

### 7.3 在战法卡里链接到匹配的股票

在战法卡笔记正文里直接写双链：

```markdown
# 近期触发标的

- 600519（2026-09-05 弱转强，2 连板）
- 000858（2026-09-04 首板）
```

保存后，股票笔记的"匹配战法"章节反向链接区会自动出现这张战法卡。

---

## 8. 日常使用工作流

### 8.1 看到一只新股票

1. **建实体**：在 `stocks/` 右键新建 → 套 `stock` 模板 → 填 frontmatter（code/name/industry/pe/pb/market_cap）。
2. **链接行业/概念**：正文写 `食品饮料`、`白酒`。若行业/概念笔记不存在，先去对应文件夹建（套 `industry`/`concept` 模板）。
3. **填财务/估值**：在 `metrics/` 和 `valuations/` 建对应周期笔记（套 `metric`/`valuation` 模板），frontmatter 的 `code` 字段填该股票代码——股票笔记里的财务/估值 Dataview 表会自动渲染这些数据。

### 8.2 读到一份新研报

1. **建研报实体**：在 `reports/` 建笔记 → 套 `report` 模板 → 填 frontmatter（title/org/researcher/publish_date/rating_change/target_price/code）。
2. **链接股票/分析师**：正文写 `600519`、`张三`。若分析师笔记不存在，去 `analysts/` 建（套 `analyst` 模板）。
3. **摘录核心观点**：在"核心观点"章节手写或粘贴研报关键论点（投资逻辑/催化剂/风险）。这是 vault 沉淀的投研知识本体，区别于代码层只存结构化字段。

### 8.3 项目出了新 spec

1. **建 spec 实体**：在 `specs/` 建笔记 → 套 `spec` 模板 → 填 frontmatter（number/title/status）。
2. **链接受影响模块**：正文写 `akshare`（用了哪个数据源）、`首板`（影响哪张战法卡）。
3. **记录决策**：正文摘录 spec 的核心决策（为什么这么定、数据支撑是什么），链接到 `specs/SNNN-*/spec.md` 源文件路径（如果 spec 在仓库里有原始 markdown）。

> 这样 vault 的 spec 实体是**决策的知识表征**（谁连谁、为什么），不是 spec 正文副本。查 spec 正文去 `specs/` 目录，查决策之间的关联来 vault。

---

## 9. 进阶：MCP 集成

### 9.1 什么是 MCP 集成

[Model Context Protocol](https://modelcontextprotocol.io/) 是 Anthropic 推的"AI agent 访问工具"协议。用 obsidian-mcp 这类 MCP server，可以让 Claude Code、opencode 等 AI agent **直接读写 vault**——列笔记、遍历图谱、跑 Dataview 查询、新建笔记。

### 9.2 选型

两条路线（详细对比和安装见 obsidian-mcp-setup.md）：

- **起步：yanxue06/obsidian-mcp**——基于 Local REST API 插件，支持图遍历、Dataview 直传、重命名重写反向链接。需要 Obsidian 保持打开。
- **升级：obsidian-mcp-pro**——直接读 vault 文件系统，支持 canvas 操作、语义搜索，不需要 Obsidian 开着。

推荐先用 yanxue06 起步，等需要 canvas 自动化或批量语义检索时升 obsidian-mcp-pro。

### 9.3 安装步骤概述

1. 装 Obsidian 的 **Local REST API** 社区插件 → 启用 → 复制 API key。
2. 在 Claude Code 里跑：
   ```bash
   claude mcp add obsidian -e OBSIDIAN_API_KEY=你的key -- npx -y @yanxue06/obsidian-mcp
   ```
3. 完全退出并重开 Claude Code → `/mcp` → 看到 `obsidian ✓ Connected`。
4. 详细配置 + 故障排除 + 工具列表见 obsidian-mcp-setup.md。

### 9.4 用 AI 做"从研报自动抽取实体灌入 vault"

接上 MCP 后，典型组合用法：

> **你**：帮我把这份茅台研报（粘贴正文）抽成 vault 实体。
>
> **AI**（Claude Code + obsidian-mcp）：读研报 → 识别出公司（贵州茅台/600519）、分析师（张三/中信）、评级（买入/目标价 2000）→ 调 obsidian-mcp 的 `create_note` 在 `reports/` 建研报笔记、`stocks/` 建股票笔记（若不存在）、`analysts/` 建分析师笔记 → 自动填 frontmatter + 写双链 → 返回新建笔记列表。

这样研报灌入从手动 5 分钟一份降到 30 秒一份，是 vault 从"骨架"走向"有血肉知识库"的关键工作流。

> 阶段 0 尚未实现自动灌入管线（需 LLM 抽取模板 + 字段映射规则），上述是目标态。手动建实体仍是当前主路径。
