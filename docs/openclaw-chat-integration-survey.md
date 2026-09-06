# OpenClaw 聊天渠道接入调研报告

> 调研日期：2026-09-06
> 调研范围：OpenClaw 官方仓库 + 文档 + ECC 生态相关 skill
> 报告目标：为知识图谱接入飞书/微信/Telegram/Discord bot 提供可借鉴的架构参考

---

## 1. OpenClaw 是什么

### 1.1 定位

OpenClaw 是一个**本地优先（local-first）的 AI 助手网关**，核心定位是：

> "Your assistant, on your devices, in your chats."

它连接 AI 模型、工具、消息渠道和可选的配套应用，通过一个 **Gateway** 统一管控。
- 个人场景：在笔记本电脑上运行作为个人助手
- 团队场景：作为共享的团队部署，配置是唯一的区别

### 1.2 核心架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        OpenClaw 架构                                │
├─────────────────────────────────────────────────────────────────────┤
│  用户界面层                                                          │
│    ├── Control UI (Web)                                             │
│    ├── CLI (`openclaw`)                                             │
│    ├── TUI (终端 UI)                                                 │
│    └── WebChat (内嵌聊天)                                             │
│                        ↕ WebSocket                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                        Gateway (核心网关)                       │ │
│  │  ├─ 会话管理 (sessions)                                        │ │
│  │  ├─ 工具调度 (tools)                                           │ │
│  │  ├─ 事件路由 (events)                                          │ │
│  │  └─ 渠道连接 (channels)                                        │ │
│  │     ├─ Telegram (内置插件)                                      │ │
│  │     ├─ Discord (官方插件)                                      │ │
│  │     ├─ Slack (官方插件)                                        │ │
│  │     ├─ Feishu/Lark (官方插件)                                  │ │
│  │     ├─ WeChat (外部插件)                                       │ │
│  │     ├─ WhatsApp (官方插件)                                    │ │
│  │     └─ ... 30+ 渠道                                           │ │
│  │                                                                 │ │
│  │  ├─ MCP 集成 (mcp.servers)                                    │ │
│  │  ├─ 模型提供方 (model providers)                               │ │
│  │  ├─ 插件系统 (plugins)                                         │ │
│  │  └─ 技能系统 (skills)                                          │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                        ↕ Plugin SDK / Channel Plugin Contract       │
│  消息渠道层                                                          │
│    ├── Telegram (grammY SDK)                                        │
│    ├── Discord (Discord Gateway)                                    │
│    ├── Slack (Socket Mode / HTTP)                                   │
│    ├── Feishu/Lark (Open Platform API)                              │
│    ├── WeChat (Tencent iLink API)                                   │
│    └── ...                                                          │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 核心能力

- **渠道抽象**：统一的 channel 接口，各渠道实现统一的消息收发协议
- **多账户支持**：每个渠道可配置多个 bot 账户
- **会话隔离**：DM/群组/话题线程级别的会话隔离
- **访问控制**：配对(pairing)/白名单(allowlist)/开放(open) 三种策略
- **工具集成**：内置工具 + MCP 服务器 + 插件工具
- **流式回复**：支持实时流式输出（streaming cards / live preview）
- **动态 Agent 创建**：每个用户自动创建隔离的 Agent 实例

---

## 2. 飞书 Bot 接入（Feishu/Lark）

### 2.1 接入方式

**官方插件**：`@openclaw/feishu`

```bash
# 安装插件
openclaw plugins install @openclaw/feishu

# 配置登录（引导式设置向导）
openclaw channels login --channel feishu
```

### 2.2 认证方式

- **App ID + App Secret**：从飞书开放平台 (`https://open.feishu.cn`) 获取
- **QR 扫码**：飞书 App 扫码自动创建 bot（锁定 DMs 到自己的账户）

### 2.3 事件传输

| 模式 | 描述 | 是否需要公网 URL |
|------|------|-----------------|
| **WebSocket（默认）** | 持久连接，实时接收事件 | 否 |
| **Webhook** | HTTP 回调接收事件 | 是 |

**WebSocket 是默认且推荐的方式**，无需公网地址即可运行。

### 2.4 双向通信

- **Inbound（接收）**：通过飞书事件订阅 `im.message.receive_v1` 接收用户消息
- **Outbound（发送）**：通过飞书 Open API 发送回复（文本、图片、文件、交互卡片）
- **Streaming**：支持飞书交互卡片流式更新（Card Kit streaming API），实现实时打字效果

### 2.5 关键配置

```json5
{
  channels: {
    feishu: {
      enabled: true,
      domain: "feishu", // 或 "lark"
      connectionMode: "websocket", // 默认，也可 "webhook"
      appId: "cli_xxx",
      appSecret: "xxx",
      
      // DM 策略
      dmPolicy: "pairing", // "pairing" | "allowlist" | "open"
      
      // 群组策略
      groupPolicy: "allowlist", // "open" | "allowlist" | "disabled"
      requireMention: true,
      
      // 流式回复
      streaming: {
        mode: "partial", // "partial" | "off"
        block: { enabled: true }
      }
    }
  }
}
```

### 2.6 消息类型支持

**接收（Inbound）**：
- ✅ 文本
- ✅ 富文本（post）
- ✅ 图片
- ✅ 文件
- ✅ 音频
- ✅ 视频
- ✅ 贴纸（sticker）

**发送（Outbound）**：
- ✅ 文本
- ✅ 图片
- ✅ 文件
- ✅ 音频（Ogg/Opus）
- ✅ 视频
- ✅ 交互卡片（支持流式更新）

### 2.7 会话管理

```json5
{
  channels: {
    feishu: {
      // 群组会话范围
      groupSessionScope: "group", // "group" | "group_sender" | "group_topic" | "group_topic_sender"
      
      // 话题线程回复
      replyInThread: "enabled", // 创建/继续话题线程
    }
  },
  session: {
    dmScope: "main" // DM 映射到主会话
  }
}
```

### 2.8 飞书特有工具

OpenClaw 为飞书提供了内置工具：
- `feishu_doc` - 文档操作
- `feishu_chat` - 聊天信息查询
- `feishu_wiki` - 知识库
- `feishu_drive` - 云存储
- `feishu_perm` - 权限管理
- `feishu_bitable_*` - Bitable/多维表格

---

## 3. 微信接入（WeChat）

### 3.1 接入方式

**外部插件**：`@tencent-weixin/openclaw-weixin`

微信接入是**外部插件**，由腾讯微信团队维护，不集成在 OpenClaw 核心仓库中。

```bash
# 安装插件
openclaw plugins install @tencent-weixin/openclaw-weixin

# 重启 Gateway
openclaw gateway restart

# QR 登录
openclaw channels login --channel openclaw-weixin
```

### 3.2 认证方式

- **QR 扫码登录**：使用手机微信扫码确认
- 插件在本地保存账户 token

### 3.3 通信方式

- **双向通信**：通过 Tencent iLink API 进行消息收发
- 支持**直接对话**（DM），群组聊天未公开宣传

### 3.4 关键限制

- 微信是**外部插件**，OpenClaw 核心保持渠道无关
- 微信登录、API 调用、媒体上传/下载、上下文 token 管理均由外部插件负责
- 插件版本与 OpenClaw 版本有兼容性要求

| 插件版本 | OpenClaw 版本 | npm tag |
|---------|--------------|---------|
| 2.x     | >=2026.5.12   | latest  |
| 1.x     | >=2026.1.0 <2026.3.22 | legacy |

---

## 4. Telegram 接入

### 4.1 接入方式

**内置插件（bundled）**，开箱即用。

```bash
# 配置 token 即可
export TELEGRAM_BOT_TOKEN="123:abc"
```

### 4.2 通信方式

- **Transport**：Long polling（默认）/ Webhook（可选）
- **SDK**：grammY

### 4.3 双向通信

- **Inbound**：Bot API `getUpdates` 长轮询获取消息
- **Outbound**：Bot API `sendMessage` 等接口发送回复
- **Streaming**：支持 live preview（`editMessageText` 实时编辑预览消息）

### 4.4 访问控制

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing", // "pairing" | "allowlist" | "open" | "disabled"
      allowFrom: ["987654321"], // 白名单用户 ID
      groupPolicy: "allowlist",
      groups: {
        "-1001234567890": {
          requireMention: true,
          allowFrom: ["8734062810"]
        }
      }
    }
  }
}
```

---

## 5. Discord 接入

### 5.1 接入方式

**官方插件（official plugin）**。

```bash
# 配置 token
export DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN"
```

### 5.2 通信方式

- **Transport**：Discord Gateway WebSocket（默认）
- **SDK**：自建 Discord Gateway 客户端

### 5.3 双向通信

- **Inbound**：Discord Gateway 接收消息事件
- **Outbound**：Discord REST API 发送消息
- **Streaming**：支持 `editMessage` 实时编辑预览

### 5.4 关键配置

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: { source: "env", provider: "default", id: "DISCORD_BOT_TOKEN" },
      
      // 特权 Intent（必须开启 Message Content Intent）
      intents: {
        messageContent: true,
        serverMembers: true,
        presence: false
      },
      
      // 群组策略
      groupPolicy: "allowlist",
      guilds: {
        "YOUR_SERVER_ID": {
          requireMention: true,
          users: ["YOUR_USER_ID"],
          roles: ["ROLE_ID"]
        }
      }
    }
  }
}
```

---

## 6. 对话流程完整链路

### 6.1 通用消息流转

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   用户发消息  │────→│ 渠道网关     │────→│   OpenClaw   │────→│   AI Agent   │
│ (飞书/微信/   │     │ (Telegram/   │     │   Gateway    │     │  (模型调用)   │
│  Telegram/   │     │ Discord/     │     │              │     │              │
│  Discord)    │     │ Slack 等)    │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────┬───────┘
     ▲                                                                  │
     │                                                                  ↓
     │  6. 发送回复         ┌──────────────┐     ┌──────────────┐
     │  ←←←←←←←←←←←←←←←←←←│  渠道网关     │←────│  回复格式化   │
     │                     │  发送回复     │     │  (卡片/文本)  │
     └─────────────────────│ 到用户        │     └──────────────┘
                           └──────────────┘
```

### 6.2 详细步骤

**Step 1：渠道事件接收**
- 各渠道通过各自 SDK/API 接收用户消息
- 消息被标准化为 OpenClaw 内部统一的消息信封格式（channel envelope）
- 包含：发送者 ID、聊天 ID、消息文本、附件、回复引用等元数据

**Step 2：访问控制检查**
- 检查 DM/群组访问策略（pairing / allowlist / open）
- 检查是否 mention bot（群组中）
- 未通过的发送者被拒绝或收到配对请求

**Step 3：会话路由**
- 根据 `session.dmScope` 配置确定会话 ID
- DM 默认映射到 `agent:main:main`
- 群组会话隔离：`agent:<agentId>:<channel>:<chatId>`
- 话题线程：`agent:<agentId>:<channel>:<chatId>:topic:<threadId>`

**Step 4：Agent 执行**
- Gateway 将消息路由到对应 Agent
- Agent 加载上下文（历史消息、工具、MCP 等）
- 调用 AI 模型生成回复
- 可能触发工具调用（文件操作、网络请求等）

**Step 5：回复格式化**
- 将 AI 回复转换为渠道特定的消息格式
- 支持 Markdown → 渠道原生格式转换
- 长消息自动分块（如 Telegram 4000 字符限制）

**Step 6：渠道发送**
- 通过渠道 API 发送回复
- 支持流式更新（飞书交互卡片、Telegram editMessageText）
- 返回发送确认

---

## 7. MCP 集成

### 7.1 MCP 是什么

> Model Context Protocol (MCP) — 代理从另一个程序借用工具的方式

OpenClaw 通过 MCP 服务器暴露工具、资源和提示，让 Agent 可以调用外部能力。

### 7.2 MCP 配置

```bash
# 添加 MCP 服务器
openclaw mcp add local-tools \
  --command node \
  --arg ./dist/mcp-server.js \
  --cwd /srv/openclaw-tools

# 验证连接
openclaw mcp doctor local-tools --probe
```

### 7.3 MCP 配置示例

```json5
{
  mcp: {
    servers: {
      docs: {
        url: "https://mcp.example.com/mcp",
        transport: "streamable-http",
        enabled: true,
        connectionTimeoutMs: 5000,
        requestTimeoutMs: 20000,
        toolFilter: {
          include: ["search", "read_*"]
        }
      }
    }
  }
}
```

### 7.4 支持三种传输方式

| 传输方式 | 描述 |
|---------|------|
| **Stdio** | 本地进程间通信 |
| **SSE** | Server-Sent Events |
| **Streamable HTTP** | 流式 HTTP |

### 7.5 与知识图谱的关联

OpenClaw 的 MCP 机制可用于：
- 暴露知识图谱查询工具（如 Neo4j 查询 MCP）
- 暴露文档检索工具（如 RAG 检索 MCP）
- 暴露外部数据源（如股票数据、新闻 API）

---

## 8. 可借鉴点

### 8.1 架构设计借鉴

| 设计 | OpenClaw 实现 | 可借鉴点 |
|------|--------------|---------|
| **Gateway 模式** | 单一网关集中管理所有渠道连接 | 我们的服务也可采用 Gateway + Channel Adapter 模式，统一处理多平台消息 |
| **Channel Plugin Contract** | 统一的渠道插件接口，核心与渠道解耦 | 飞书/微信/Telegram/Discord 等接入可复用同一套接口 |
| **配置即代码** | JSON5 配置驱动所有行为 | 渠道接入策略、访问控制、回复方式全部可配置 |
| **多账户支持** | 每个渠道支持多 bot 账户 | 同一平台可配置多个 bot，隔离不同业务场景 |

### 8.2 飞书 Bot 具体借鉴

1. **WebSocket 优先**：无需公网即可运行，降低部署门槛
2. **流式卡片回复**：飞书交互卡片支持实时更新，体验更好
3. **会话隔离**：`groupSessionScope` 支持多种会话映射模式
4. **话题线程**：`replyInThread` 保持上下文连续性
5. **动态 Agent 创建**：`dynamicAgentCreation` 自动为每个用户创建隔离 Agent

### 8.3 可复用组件

| 组件 | 复用建议 |
|------|---------|
| **Channel Envelope 标准化** | 定义统一的消息信封格式，各渠道适配器负责转换 |
| **Access Control 层** | pairing/allowlist/open 三级策略可直接复用 |
| **Session Router** | 按渠道+聊天+用户路由会话的通用逻辑 |
| **Streaming Reply** | 飞书/ Telegram 的流式回复机制 |
| **Tool Integration** | MCP 集成模式可用于接入知识图谱工具 |

### 8.4 知识图谱 + Bot 接入建议

基于 OpenClaw 的经验，建议我们的知识图谱 bot 架构：

```
┌─────────────────────────────────────────────────────────────┐
│                      Bot Gateway                              │
│  ├─ Feishu Adapter（飞书 Open Platform API）                   │
│  ├─ WeChat Adapter（企业微信/个人微信）                         │
│  ├─ Telegram Adapter（Bot API）                               │
│  ├─ Discord Adapter（Gateway API）                          │
│  └─ ...                                                       │
│                        ↕                                      │
│  ├─ Message Normalizer（统一信封格式）                          │
│  ├─ Access Control（pairing/allowlist/open）                 │
│  ├─ Session Router（会话路由）                                │
│  └─ Tool Dispatcher（工具调度）                              │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                      AI Agent Core                            │
│  ├─ LLM 调用                                                  │
│  ├─ MCP Server（知识图谱查询、文档检索等）                      │
│  └─ Memory / Context 管理                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. ECC 生态相关 Skill

### 9.1 本地发现的 Skill

| Skill | 描述 | 与 OpenClaw 关系 |
|-------|------|-----------------|
| `social-publisher` | 13 平台 SocialClaw 发布 | 外部服务，非 OpenClaw 核心 |
| `social-publishing` | SocialClaw API 包装 | 外部服务，非 OpenClaw 核心 |
| `openclaw-persona-forge` | OpenClaw 人格锻造 | 与 OpenClaw 直接相关 |

### 9.2 本地 opencode.json 配置

在 `~/.config/opencode/opencode.json` 中发现了 MCP 配置：

- **context7**：文档查询 MCP
- **github**：GitHub MCP
- **memory**：记忆 MCP
- **playwright**：浏览器 MCP
- **codegraph**：代码图 MCP
- 多个 AI 模型 provider（Bailian、OmniRoute 等）

---

## 10. 总结

### 10.1 OpenClaw 聊天渠道接入特点

1. **渠道插件化**：30+ 渠道通过插件架构接入，核心保持渠道无关
2. **配置驱动**：所有行为通过 JSON5 配置控制
3. **访问控制完善**：pairing/allowlist/open 三级策略
4. **会话隔离灵活**：支持 DM/群组/话题线程多级别隔离
5. **流式回复**：支持实时流式输出，提升用户体验
6. **MCP 原生集成**：通过 MCP 协议扩展 Agent 能力

### 10.2 对我们接知识图谱到飞书/微信 bot 的启示

1. **采用 Gateway + Adapter 模式**：统一处理多平台接入
2. **WebSocket 优先飞书接入**：无需公网，部署简单
3. **微信作为外部插件**：核心与微信解耦，插件化接入
4. **统一消息信封**：各渠道适配器负责标准化
5. **MCP 暴露知识图谱工具**：通过 MCP 让 Agent 查询知识图谱
6. **会话隔离**：每个用户独立会话，保证上下文隔离
7. **流式回复**：飞书交互卡片实时更新，提升体验

---

## 附录：OpenClaw 渠道支持列表

截至 2026 年 9 月，OpenClaw 官方文档列出支持的渠道：

| 渠道 | 状态 | 类型 |
|------|------|------|
| Telegram | 内置插件 (bundled) | 官方 |
| Discord | 官方插件 (official) | 官方 |
| Slack | 官方插件 (official) | 官方 |
| Feishu/Lark | 官方插件 (official) | 官方 |
| WeChat | 外部插件 (external) | 腾讯 |
| WhatsApp | 官方插件 (official) | 官方 |
| iMessage | 官方插件 (official) | 官方 |
| Signal | 官方插件 (official) | 官方 |
| Google Chat | 官方插件 (official) | 官方 |
| LINE | 官方插件 (official) | 官方 |
| Matrix | 官方插件 (official) | 官方 |
| Mattermost | 官方插件 (official) | 官方 |
| Microsoft Teams | 官方插件 (official) | 官方 |
| IRC | 官方插件 (official) | 官方 |
| SMS | 官方插件 (official) | 官方 |
| Twitch | 官方插件 (official) | 官方 |
| WebChat | 核心内置 (core) | 官方 |
| Zalo | 官方插件 (official) | 官方 |
| Nostr | 官方插件 (official) | 官方 |
| ... | ... | ... |

---

*报告生成时间：2026-09-06*
*数据来源：OpenClaw GitHub 仓库、官方文档 (docs.openclaw.ai)、本地 ECC 生态配置*
