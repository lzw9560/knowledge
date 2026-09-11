# 飞书/微信 Bot 对话知识图谱方案

> 让你在飞书/微信里直接和投研知识图谱对话——"查白酒行业所有股票的 PE 排序"、"600519 关联哪些战法和数据源"、"本周图谱新增了什么"。

## 设计依据

- **OpenClaw 调研**（`docs/openclaw-chat-integration-survey.md`）：Gateway + Channel Adapter 架构，飞书 WebSocket 双向，微信 Tencent iLink API，MCP 原生集成
- **Vibe-Research 已有**：`backend/notification/senders/feishu_sender.py`（lark-oapi SDK，双向 App Bot）+ `wechat_sender.py`（企业微信 webhook，单向）+ `chat.py`（AI 对话层，5 工具 function-calling）+ `mcp_server.py`（MCP 5 工具）
- **Obsidian MCP**（`docs/obsidian-mcp-setup.md`）：yanxue06/obsidian-mcp（25 工具，含 `query_dataview`/`traverse_graph`/`find_orphans`）

## 架构

```
飞书/微信用户发消息
        │
        ▼
┌───────────────────┐
│ Channel Adapter   │  飞书: lark-oapi WebSocket (复用 feishu_sender 的 SDK)
│ (渠道适配器)        │  微信: 企业微信回调事件 (需新增，现有 wechat_sender 是单向)
└────────┬──────────┘
         │ 标准化消息信封 (user_id, text, channel)
         ▼
┌───────────────────┐
│ Chat Gateway      │  复用 Vibe-Research chat.py 的 AI 对话层
│ (对话网关)         │  SYSTEM_PROMPT 加知识图谱查询能力
└────────┬──────────┘
         │ function-calling 调工具
         ▼
┌───────────────────┐
│ Tool Layer        │  原有 5 工具(query_quote/valuation/reports/news/global_stock)
│ (工具层)          │  + 新增知识图谱工具:
│                   │    query_kg_entities(类型, 过滤) → Dataview 查询
│                   │    query_kg_relations(实体, 关系) → traverse_graph
│                   │    kg_audit() → find_orphans + find_broken_links
└────────┬──────────┘
         │ 工具调 Obsidian MCP (yanxue06) 或直接读 vault markdown
         ▼
┌───────────────────┐
│ Knowledge Graph   │  /Users/lizhiwei/Documents/Obsidian Vault/
│ (知识图谱)        │  10_Reference/investing/ 下的 markdown + [[]] + frontmatter
└───────────────────┘
         │ AI 回答
         ▼
┌───────────────────┐
│ Response Formatter│  飞书: 交互卡片(支持流式更新)
│ (回复格式化)      │  微信: markdown 文本(企业微信支持)
└───────────────────┘
```

## 两条实现路径

### 路径 A：复用 Vibe-Research 后端（推荐，最快）

Vibe-Research 已有 FastAPI(:8900) + chat.py + 飞书 sender + MCP server。加一个 `/api/bot/feishu` 路由接收飞书事件 + 扩展 chat.py 的 TOOLS 加知识图谱查询工具。

**改动量**：中等。新增 1 个路由文件 + 扩展 TOOLS + 飞书事件订阅配置。

**优点**：复用已有 AI 对话层 + 数据工具 + 飞书 SDK，不重复造轮子。

**缺点**：Vibe-Research 后端要常驻运行（它已经是 daemon，不是问题）。

### 路径 B：独立轻量 bot 服务（借鉴 OpenClaw）

写一个独立的 Python 服务，只做 bot 网关 + Obsidian MCP 调用，不依赖 Vibe-Research 全栈。

**改动量**：大。新项目。

**优点**：轻量，不耦合 Vibe-Research。

**缺点**：重复实现 AI 对话层 + 数据工具。

### 推荐：路径 A

## 落地步骤

### 飞书（先做，双向通信最成熟）

1. **飞书开放平台建应用**
   - https://open.feishu.cn 创建企业自建应用
   - 开启"机器人"能力
   - 权限：`im:message`（收发消息）+ `im:message.group_at_msg`（群@消息）
   - 事件订阅：消息接收（`im.message.receive_v1`）
   - 通信方式：长连接（WebSocket，无需公网回调，复用 OpenClaw 的模式）

2. **Vibe-Research 加飞书 bot 路由**
   - `backend/routers/feishu_bot.py`：接收飞书事件，调 chat.py
   - 复用 `feishu_sender.py` 的 lark-oapi SDK（它已支持 App Bot 模式）
   - 环境变量：`FEISHU_APP_ID` + `FEISHU_APP_SECRET` + `FEISHU_CHAT_ID`（已有 config 映射）

3. **chat.py TOOLS 扩展知识图谱查询**
   - 新增工具 `query_kg`：参数 `query_type`(entities/relations/audit) + `filter`(类型/代码/行业)
   - 实现：调 Obsidian MCP 的 `query_dataview` 或直接 Python 读 vault markdown
   - SYSTEM_PROMPT 加知识图谱能力描述

4. **测试**
   - 飞书群里@bot 发"查白酒行业所有股票"
   - bot 调 `query_kg(entities, filter:industry=白酒)` → 返回 Dataview 结果
   - 格式化为飞书交互卡片回复

### 微信（后做，企业微信 webhook 是单向）

1. **企业微信建应用机器人**
   - 企业微信管理后台 → 应用管理 → 自建应用 → 开启机器人
   - 接收消息：需配置回调 URL（要公网或内网穿透）

2. **双向通信限制**
   - 企业微信 webhook 是**单向推送**（只能发不能收）
   - 双向需用"应用回调"模式（配接收消息 URL）
   - 如无公网，用 Cloudflare Tunnel / ngrok 穿透

3. **复用 Vibe-Research 的 wechat_sender**
   - 现有是单向 webhook，加回调接收能力
   - 或用 Server酱/PushPlus 做轻量替代（单向查图谱结果推送）

## 工具层设计（chat.py TOOLS 扩展）

### 新增 3 个知识图谱工具

```python
# 注册到 ai/tools/registry.py
{
    "name": "query_kg_entities",
    "description": "查询知识图谱实体。可按类型/行业/代码过滤。如'查白酒行业所有股票'、'查所有数据源'。",
    "parameters": {
        "type": "object",
        "properties": {
            "entity_type": {"type": "string", "enum": ["stock","industry","concept","strategy","data_source","spec","event"]},
            "filter_field": {"type": "string", "description": "过滤字段，如 industry/code/edge_family"},
            "filter_value": {"type": "string", "description": "过滤值"}
        }
    }
}

{
    "name": "query_kg_relations",
    "description": "查询实体关系。如'600519 关联哪些战法'、'国产芯片概念有哪些股票'。",
    "parameters": {
        "type": "object",
        "properties": {
            "entity_code": {"type": "string", "description": "实体代码或名称"},
            "relation_type": {"type": "string", "enum": ["belongs_to","tagged","covered_by","matches","affects"]}
        }
    }
}

{
    "name": "kg_audit",
    "description": "知识图谱健康检查。查孤立实体/断链/覆盖率。",
    "parameters": {"type": "object", "properties": {}}
}
```

### 工具实现（调 Obsidian MCP 或直接读 vault）

两种实现方式：

**方式 1：调 Obsidian MCP**（需 Obsidian 运行 + Local REST API 插件）
```python
# 通过 MCP 调 query_dataview
async def query_kg_entities(args):
    dql = f'TABLE code, name, industry FROM "10_Reference/investing/stocks" WHERE type = "stock"'
    if args.get("filter_field") == "industry":
        dql += f' AND industry = "{args["filter_value"]}"'
    # 调 MCP: query_dataview(dql)
    result = await mcp_client.call_tool("obsidian", "query_dataview", {"query": dql})
    return result
```

**方式 2：直接 Python 读 vault markdown**（不依赖 Obsidian 运行，更稳）
```python
import frontmatter  # python-frontmatter 库
from pathlib import Path

VAULT = Path("/Users/lizhiwei/Documents/Obsidian Vault/10_Reference/investing")

async def query_kg_entities(args):
    folder = args["entity_type"] + "s"  # stock → stocks
    results = []
    for f in (VAULT / folder).glob("*.md"):
        post = frontmatter.load(f)
        if args.get("filter_field"):
            if post.get(args["filter_field"]) != args["filter_value"]:
                continue
        results.append({"code": post.get("code"), "name": post.get("name"), "path": str(f)})
    return results
```

**推荐方式 2**——不依赖 Obsidian 运行，Vibe-Research 后端直接读 vault 文件。

## 对话示例

```
用户: 查白酒行业所有股票的 PE 排序
Bot:  [调 query_kg_entities(stock, industry=白酒) → 5 只股票]
      [调 query_quote(5 个代码) → 实时行情含 PE]
      白酒行业 PE 排序（截至 2026-09-06 15:00）：
      1. 五粮液(000858) PE 22.3
      2. 贵州茅台(600519) PE 25.0
      ...

用户: 600519 关联哪些战法和数据源？
Bot:  [调 query_kg_relations(600519) → traverse_graph 1 跳]
      贵州茅台(600519) 关联：
      - 行业: [[10_Reference/investing/industries/白酒]]
      - 概念: [[10_Reference/investing/concepts/高端白酒]]
      - 战法: [[strategies/low_absorption]]（低吸龙头）
      - 数据源: [[data-sources/tencent]] [[data-sources/eastmoney-push2]]

用户: 本周图谱新增了什么？
Bot:  [调 kg_audit() → git log --since="7 days ago" --oneline]
      本周图谱变更：
      - 新增 11 只股票实体（5 代表股 + 6 新建）
      - 新增 3 个行业 + 3 个概念
      - orphan_check: 7 个孤立数据源（待补链接）
```

## 合规对齐

- Vibe-Research 弱合规：bot 只查客观数据 + 知识图谱关系，不给买卖建议
- SYSTEM_PROMPT 保持投研五维框架，bot 回答挂"历史统计特征，市场有风险"
- 私有数据隔离：bot 不读 `~/.vibe-research/`（持仓/API key）

## 前置条件

| 条件 | 飞书 | 微信 |
|---|---|---|
| 开放平台账号 | 飞书开放平台 | 企业微信管理后台 |
| 应用类型 | 企业自建应用 + 机器人 | 自建应用 |
| 通信方式 | WebSocket 长连接（无需公网） | 回调 URL（需公网或穿透） |
| SDK | lark-oapi（已装） | requests（已有） |
| 环境变量 | FEISHU_APP_ID/SECRET/CHAT_ID（已有映射） | WECHAT_WEBHOOK_URL（已有） |

## 优先级

1. **先做飞书**——双向通信最成熟（WebSocket），Vibe-Research 已有 lark-oapi SDK + App Bot 模式
2. **微信延后**——企业微信 webhook 是单向，双向需公网回调，复杂度高
3. **工具层先行**——先把 3 个知识图谱查询工具加到 chat.py 的 TOOLS，不依赖 bot 也能在 Vibe-Research 前端"问 AI"里用

---

**Version:** 1.0.0
**依据:** OpenClaw 调研 + Vibe-Research 已有基础设施
**作者:** lzw9560
