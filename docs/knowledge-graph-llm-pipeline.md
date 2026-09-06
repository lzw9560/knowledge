# LLM 知识抽取 Pipeline 架构设计

> 把 Vibe-Research 项目的存量知识（spec/代码/战法/数据源）自动抽取到 Obsidian 知识图谱 vault 的 pipeline 设计。
> 方法论对齐 `ontology-knowledge-graph` skill 四构件（实体/关系/逻辑规则/动作）+ Curated 质量门 + 四层关系推断 + ReAct 审查。
> 借鉴 nano-ontoprompt（MIT）的 Pipeline Mapping 思路，落地到 markdown + `[[]]` + Dataview + MCP，不引入 Neo4j/Postgres 重栈。

---

## 目录

1. [Pipeline 总体架构](#1-pipeline-总体架构)
2. [实体词典设计](#2-实体词典设计)
3. [抽取 Prompt 设计](#3-抽取-prompt-设计)
4. [消歧与归一策略](#4-消歧与归一策略)
5. [链接一致性保障](#5-链接一致性保障)
6. [增量同步策略](#6-增量同步策略)
7. [与 MCP 的集成](#7-与-mcp-的集成)
8. [合规与风险](#8-合规与风险)
9. [技术选型](#9-技术选型)
10. [分阶段实施计划](#10-分阶段实施计划)

---

## 1. Pipeline 总体架构

### 数据流

```
┌─────────────────────────────────────────────────────────────────┐
│  输入源（Vibe-Research 项目存量知识）                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ specs/   │  │backend/  │  │strategies│  │ARCHITECTURE/  │  │
│  │60+ spec  │  │代码+模型 │  │cards/    │  │VISION/decision│  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬────────┘  │
│       │             │             │               │            │
└───────┼─────────────┼─────────────┼───────────────┼────────────┘
        ▼             ▼             ▼               ▼
┌───────────────────────────────────────────────────────────────┐
│  解析层（输入解析器）                                          │
│  - spec 解析：读 spec.md → {编号,标题,状态,受影响文件}        │
│  - 代码解析：AST 扫 Pydantic 模型 → {实体类,字段}             │
│  - 文档解析：ARCHITECTURE.md 分段 → {数据源,数据流}           │
│  - 战法解析：读 cards/*.md → {战法名,入场条件,edge_family}    │
└───────────────────────────┬───────────────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  抽取层（规则优先，LLM 兜底）                                  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ L1 规则抽取（结构化输入）                                │  │
│  │ - spec README 表格 → 直接提取 spec 实体                  │  │
│  │ - ARCHITECTURE 数据流段 → 直接提取数据源实体            │  │
│  │ - Pydantic 模型 AST → 直接提取字段 schema                │  │
│  │ - 战法卡 frontmatter → 直接提取战法属性                  │  │
│  └──────────────────────┬──────────────────────────────────┘  │
│                         ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ L2 LLM 抽取（非结构化输入）                               │  │
│  │ - spec 正文 → 抽取决策关系/受影响模块/验收标准           │  │
│  │ - decision-log → 抽取 DEC 决策/被否决方案                │  │
│  │ - 代码注释 → 抽取数据流关系/限流策略                     │  │
│  │ - 研报/新闻 → 抽取公司/行业/事件实体                      │  │
│  └──────────────────────┬──────────────────────────────────┘  │
└───────────────────────────┬───────────────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  质量门（Curated）—— inbox/ 文件夹                           │
│  - L1 规则抽取 → 直接进正式区（confidence: high）             │
│  - L2 LLM 抽取 → 进 inbox/（confidence: low/medium）         │
│  - 质量评分：完整度30% + 一致性25% + 链接度25% + 溯源20%      │
│  - ≥60 分 → mv 到正式区 + approved_date                        │
│  - <60 分 → 留 inbox 标 rejected + reject_reason              │
└───────────────────────────┬───────────────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  关系推断层（四层渐进）                                        │
│  L1 精确外键（代码匹配）→ 直接建链                            │
│  L2 值格式容错（去分隔符）→ 直接建链                          │
│  L3 备用键（别名表）→ 进 inbox，confidence: medium            │
│  L4 LLM 语义推断 → 进 inbox，confidence: low                   │
└───────────────────────────┬───────────────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  vault 写入层                                                  │
│  - 生成 markdown 文件（对应实体类型文件夹）                    │
│  - 填 YAML frontmatter（type/code/name/confidence/source）     │
│  - 写 [[]] 双向链接（查实体词典保证目标存在）                 │
│  - 更新 index.md 的 Dataview 查询                              │
└───────────────────────────┬───────────────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  一致性校验层                                                   │
│  - find_broken_links（断链检测）                               │
│  - find_orphans（孤立实体检测）                                │
│  - duplicate_check（同 code 查重）                             │
│  - 生成校验报告到 reviews/                                      │
└───────────────────────────────────────────────────────────────┘
```

### 关键设计决策

| 决策 | 选择 | 理由 | 被否决方案 |
|---|---|---|---|
| 抽取策略 | **规则优先，LLM 兜底** | 项目存量是结构化文档（spec 表格/AST/frontmatter），规则抽取准确率 100%；LLM 只处理非结构化段落 | 全 LLM 抽取——对结构化输入过度，且准确率不可控 |
| 质量门位置 | **inbox/ 文件夹** | 隔离未审实体，不污染正式图谱 | 直接灌入——噪声不可逆 |
| 关系推断 | **四层渐进** | 精确层先做，模糊层兜底，L4 标 confidence | 只用 LLM——准确度低 |
| 写入方式 | **直接写文件 + MCP 辅助** | Python 脚本直接写 markdown，MCP 用于一致性校验 | 全 MCP——create_note 逐个太慢 |

---

## 2. 实体词典设计

实体词典是链接一致性的核心——同一家公司"贵州茅台"/"茅台"/"600519"/"Moutai"必须归一到同一 vault 文件。

### 数据结构

```json
{
  "aliases": {
    "贵州茅台": {"path": "10_Reference/investing/stocks/600519", "type": "stock"},
    "茅台": {"path": "10_Reference/investing/stocks/600519", "type": "stock"},
    "600519": {"path": "10_Reference/investing/stocks/600519", "type": "stock"},
    "Moutai": {"path": "10_Reference/investing/stocks/600519", "type": "stock"},
    "S007": {"path": "10_Reference/investing/specs/S007", "type": "spec"},
    "契约层": {"path": "10_Reference/investing/specs/S007", "type": "spec"},
    "腾讯行情": {"path": "10_Reference/investing/data-sources/tencent", "type": "data_source"},
    "qt.gtimg.cn": {"path": "10_Reference/investing/data-sources/tencent", "type": "data_source"}
  },
  "by_type": {
    "stock": ["600519", "000858", ...],
    "spec": ["S001", "S002", ...],
    "data_source": ["tencent", "eastmoney-push2", ...]
  }
}
```

### 初始化

词典从两个源初始化：

1. **已有 vault 文件**：扫描 `10_Reference/investing/*/` 下的所有 .md 文件，读 frontmatter 的 `code`/`name`/别名，建初始词典
2. **Vibe-Research 数据源**：
   - `astock.py` 的 `individual_info()` 函数 → A 股股票代码+名称
   - `specs/README.md` 的 spec 编号表
   - `ARCHITECTURE.md` 的数据源清单

### 存储

词典存 vault 内 `10_Reference/investing/.entity-dictionary.json`（git 追踪，各设备同步）。

### 增量更新

新实体出现时：
1. LLM/规则抽取产出新实体
2. 查词典——已有则用规范名建 `[[]]` 链接
3. 词典无——先建 stub 文件到 inbox/，再追加词典条目

---

## 3. 抽取 Prompt 设计

### 针对不同输入源的 prompt

**P1：spec 决策抽取 prompt**

```markdown
你是一位投研知识图谱工程师。请从以下 SDD spec 中抽取决策实体和关系。

## 输入
spec 编号：{number}
spec 标题：{title}
spec 正文：
{spec_content}

## 约束
- 实体类型限定：只能抽取 spec / data_source / strategy 三类
- 关系类型限定：affects / depends_on / replaces / superseded_by
- 不臆造：spec 正文没有的不要编

## 输出格式（JSON）
{
  "entities": [
    {"type": "spec", "number": "S007", "title": "...", "status": "...", "source": "specs/S007/spec.md"}
  ],
  "relations": [
    {"from": "S007", "relation": "affects", "to": "data_source/akshare", "confidence": "high"}
  ]
}
```

**P2：研报抽取 prompt**

```markdown
你是一位投研知识图谱工程师。请从以下研报中抽取实体和关系。

## 输入
研报标题：{title}
研报机构：{org}
研报正文：
{report_content}

## 约束
- 实体类型限定：stock / industry / concept / analyst / metric / event
- 关系类型限定：belongs_to / tagged / covered_by / has_metric / authored_by
- 股票优先用代码（6位数字），不确定标 confidence: low
- 所有抽取结果标 source: "report:{title}"

## 输出格式（JSON）
{
  "entities": [
    {"type": "stock", "code": "600519", "name": "贵州茅台", "confidence": "high", "source": "report:xxx"}
  ],
  "relations": [
    {"from": "600519", "relation": "belongs_to", "to": "industry/白酒", "confidence": "high"}
  ]
}
```

**P3：代码注释抽取 prompt**

```markdown
请从以下 Python 代码中抽取数据流关系。

## 输入
文件：{file_path}
代码：
{code_content}

## 约束
- 只抽取：函数→数据源 的调用关系、Pydantic 模型→字段 的 schema
- 不臆造：代码里没有的函数/字段不要编
- 关系类型：calls / defines / feeds_into

## 输出格式（JSON）
{
  "entities": [
    {"type": "data_source", "name": "tencent", "source": "astock.py:tencent_quote"}
  ],
  "relations": [
    {"from": "astock.tencent_quote", "relation": "calls", "to": "data_source/tencent", "confidence": "high"}
  ]
}
```

---

## 4. 消歧与归一策略

| 实体类型 | 消歧键 | 策略 |
|---|---|---|
| **股票** | 6位代码（主）/ 名称（备） | 代码唯一；名称歧义（"茅台"可能指股份或集团）时查实体词典 |
| **行业** | 行业名 | 证监会分类 vs 概念板块分开存（industries/ vs concepts/） |
| **分析师** | 机构+姓名（联合键） | 同名不同机构视为不同人 |
| **spec** | SNNN 编号 | 编号唯一 |
| **数据源** | endpoint 域名 | 域名唯一 |
| **战法** | 战法卡文件名 | 文件名唯一 |

### 置信度标注

所有抽取结果必须标 confidence：
- `high`：L1 精确匹配 / 规则抽取 / 代码 AST
- `medium`：L3 备用键匹配 / LLM 从结构化段落抽取
- `low`：L4 LLM 语义推断 / 非结构化文本抽取

low confidence 的实体/关系**必须进 inbox**，不能直接进正式区。

---

## 5. 链接一致性保障

### 链接生成流程

```
LLM/规则产出实体 → 查实体词典
  ├─ 词典有 → 用规范路径建 [[规范路径]]
  └─ 词典无 → 建 stub 文件到 inbox/（最小 frontmatter + "待补充"）
              → 追加词典条目
              → 用新路径建 [[新路径]]
```

### Stub 文件模板

```markdown
---
type: stock
code: {code}
name: {name}
confidence: low
source: {source}
quality_score: 0
approved: false
created: {date}
---

# {name}

> 此实体由 pipeline 自动生成 stub，待人工补充。

（待补充内容）
```

### 一致性校验（pipeline 末尾）

1. `find_broken_links`（MCP）：扫所有 `[[]]`，目标不存在则报 high 级问题
2. `find_orphans`（MCP）：无入边实体报 medium 级问题
3. `duplicate_check`（Dataview）：按 code 分组，同 code 多份报 critical
4. 结果写到 `reviews/<date>-pipeline-audit.md`

---

## 6. 增量同步策略

### 首次全量灌入

```
扫描源                    → 抽取内容                    → 目标文件夹
specs/README.md 表格      → 60+ spec 实体               → specs/
specs/decision-log.md    → 5 DEC 决策实体              → specs/
ARCHITECTURE.md 数据流段  → 16 数据源实体               → data-sources/  ✅ 已完成
backend/strategies/cards/ → 12 战法卡                    → strategies/    ✅ 已完成
backend/models/*.py      → Pydantic 模型 schema        → 各实体模板字段
backend/data/sources/    → 数据源函数→数据源实体关系     → data-sources/
ARCHITECTURE.md 模块清单  → 后端模块实体                 → (待建 modules/)
```

### 增量更新

**触发**：git commit 到 Vibe-Research 仓

**流程**：
1. `git diff HEAD~1 --name-only` 取变更文件列表
2. 按类型分流：
   - `specs/SNNN-*/*.md` 变更 → 重抽该 spec 实体
   - `backend/strategies/cards/*.md` 变更 → 重抽战法卡
   - `backend/data/sources/*.py` 变更 → 重抽数据源关系
   - `ARCHITECTURE.md` 变更 → 重抽数据流
3. 对比已有 vault 实体，增量更新（不重写未变的）

### 冲突处理

同一实体被多个源抽取时，优先级：
1. **spec 决策**（最高，是项目设计意图）
2. **代码 AST**（实际实现）
3. **文档注释**（可能过时）
4. **LLM 推断**（最低，标 confidence: low）

---

## 7. 与 MCP 的集成

### 选型

- **起步**：`yanxue06/obsidian-mcp`（25 工具，含 `traverse_graph`/`query_dataview`/`move_note`/`find_orphans`）
- **升级**：`obsidian-mcp-pro`（41 工具，加 `search_semantic`/canvas）

### pipeline 调用 MCP 的场景

| MCP 工具 | 用途 | 调用时机 |
|---|---|---|
| `get_vault_guide()` | LLM 先学 vault 规范再写 | pipeline 启动时 |
| `create_note(path, content)` | 创建新实体 | 抽取产出新实体时 |
| `upsert_note(path, content)` | 更新已有实体 | 增量同步时 |
| `move_note(old, new)` | 实体改名（自动重写反向链接） | 股票改名/spec 重新编号时 |
| `find_broken_links()` | 断链检测 | pipeline 末尾校验 |
| `find_orphans()` | 孤立实体检测 | pipeline 末尾校验 |
| `query_dataview(dql)` | 一致性查询 | 查"所有无 industry 的股票"等 |
| `traverse_graph(path, depth)` | 影响范围分析 | 实体变更时看下游影响 |

### 不用 MCP 的场景

- 批量灌入（首次 60+ spec）——直接 Python 写文件，比 `create_note` 逐个快
- 实体词典维护——纯 JSON 操作，不需 MCP
- 规则抽取（spec 表格/AST）——纯解析，不需 LLM/MCP

---

## 8. 合规与风险

### Vibe-Research 核心原则对齐

| 原则（VISION.md） | pipeline 落地 |
|---|---|
| 不臆造数据 | LLM 抽取的属性若来自推测而非源文本，标 confidence: low + "待验证" |
| 私有数据隔离 | 持仓/API key/`.vibe-research/` 内容绝不进 vault |
| 不给买卖建议 | 只抽取事实性实体和关系，不抽取"买入/卖出"信号 |

### 数据安全

- pipeline 不读 `~/.vibe-research/`（用户私有数据目录）
- pipeline 不读 `.env`（API key）
- LLM 调用走用户自己的 API key，不经第三方

---

## 9. 技术选型

| 组件 | 选择 | 理由 | 被否决方案 |
|---|---|---|---|
| 抽取模型 | **本地 Ollama（qwen2.5/deepseek）** | 投研文本中文为主，本地模型够用；隐私不外泄 | 云端 API——成本高 + 数据出域 |
| 脚本语言 | **Python** | 复用 Vibe-Research 已有生态（Pydantic/akshare） | Node——MCP 生态好但项目是 Python |
| 调度 | **复用 Vibe-Research scheduled_tasks.py** | 项目已有 cron + SQLite 持久化调度 | 独立 cron——重复造轮子 |
| 关系存储 | **markdown + [[]] + frontmatter** | Obsidian 原生，可导航 | Neo4j——重栈，Obsidian 不可读 |

### 抽取模型备选

- **qwen2.5:7b**（Ollama）：中文理解好，7B 够用抽取任务
- **deepseek-coder-v2:16b**：代码理解强，适合从 Python 代码抽 schema
- **云端备选**：处理大批量时用 deepseek-chat API（成本极低）

---

## 10. 分阶段实施计划

### P1：手工验证抽取 prompt（当前可做）

**输入**：1 个 spec（如 S002 打板工作流）
**动作**：手工喂 spec 正文给 LLM，用 P1 prompt 抽取
**产出**：spec 实体 + 关系 JSON
**验收**：抽取的实体/关系与 spec README 表格一致

### P2：批量灌入 spec 实体（进行中）

**输入**：60+ spec README 表格
**动作**：规则脚本抽取（不 LLM），直接生成 spec 实体 .md
**产出**：specs/ 下 60+ 实体文件
**验收**：`find_orphans` 无新增孤立 / `find_broken_links` 无断链

### P3：灌入代码层实体

**输入**：`backend/models/*.py`（Pydantic 模型）
**动作**：AST 扫描，提取模型字段 → 更新各实体模板的 frontmatter schema
**产出**：模板字段与代码契约对齐
**验收**：模板字段数 = Pydantic 模型字段数

### P4：灌入关系层

**输入**：`backend/data/sources/*.py` + `ARCHITECTURE.md` 数据流
**动作**：规则抽取函数→数据源调用关系，建 `[[]]` 链接
**产出**：data-sources/ 实体的入边增加（被 spec/模块引用）
**验收**：`relation_density` 检查无孤岛

### P5：增量同步上线

**输入**：Vibe-Research git commit hook
**动作**：commit 触发 → `git diff` 取变更文件 → 增量抽取 → 更新 vault
**产出**：自动同步机制运转
**验收**：新 spec 落地后 24h 内 vault 自动更新

---

## 参考

- `ontology-knowledge-graph` skill（四构件方法论 + Curated 质量门 + 四层推断 + ReAct 审查）
- [nano-ontoprompt](https://github.com/jingw2/nano-ontoprompt)（MIT，Pipeline Mapping 思路来源）
- vault 结构：`/Users/lizhiwei/Documents/Obsidian Vault/10_Reference/investing/`
- MCP 选型：`docs/obsidian-mcp-setup.md`
- 已灌入实体：16 数据源（`data-sources/`）+ 12 战法卡（`strategies/`）+ spec/DEC（`specs/`，fix-7 灌入中）

---

**Version:** 1.0.0
**作者:** lzw9560
**对齐:** ontology-knowledge-graph skill 四构件 + nano-ontoprompt 方法论
