# Vibe-Research Obsidian MCP 连接配置

> 本文档讲怎么把 Obsidian vault 接入 MCP（Model Context Protocol），让 Claude Code 等 AI agent 能直接读写 `knowledge/` vault。配套文档：obsidian-vault-guide.md 讲 vault 内操作。
>
> 命令均为可复制粘贴执行。涉及具体插件版本/工具参数不确定处标注"待验证"。

---

## 1. MCP 选型说明

### 1.1 六个 Obsidian MCP server 对比

社区目前有多个 Obsidian MCP server 实现，主流候选：

| MCP server | 接入方式 | 核心能力 | 依赖 Obsidian 开着 | 备注 |
|---|---|---|---|---|
| **yanxue06/obsidian-mcp** | Local REST API 插件 | 图遍历 / Dataview 直传 / 重命名重写反向链接 / 查孤儿笔记 | 是 | 起步推荐 |
| **obsidian-mcp-pro** | 直读文件系统 | canvas 操作 / 语义搜索 / 批量索引 | 否 | 升级选项 |
| mark3labs/obsidian-mcp | Local REST API | 基础读写 | 是 | 功能较简 |
| another-guy/obsidian-mcp | Local REST API | 基础读写 | 是 | 早期实现 |
|smithery-ai/obsidian | Local REST API | 基础读写 | 是 | Smithery 注册表版本 |
| heinwer/obsidian-mcp | 直读文件系统 | 基础读写 | 否 | 文件系统直读 |

> 表中部分实现的能力描述基于各项目 README 摘要，具体工具集请以各自仓库最新文档为准——标注"待验证"的能力在升级前再核对一遍。

### 1.2 推荐路线

**yanxue06/obsidian-mcp 起步 → obsidian-mcp-pro 升级**。

### 1.3 选型理由

选 yanxue06 起步的三个理由：

1. **图遍历**：`traverse_graph` 工具能从任意笔记出发遍历 N 度双链——这是 vault 作为"知识图谱"最核心的查询能力，基础读写类 server 没有。
2. **Dataview 直传**：`query_dataview` 工具直接把 DQL 查询发给 Obsidian 跑并返回结果，复用 vault 里已有的所有 ```dataview 查询逻辑，不用在 agent 侧重写。
3. **重命名重写反向链接**：`move_note`/`rename` 操作会自动更新所有指向该笔记的 `[[]]` 链接——纯文件系统直读类 server 重命名后反向链接会断，yanxue06 经 Obsidian 处理不会。

升级到 obsidian-mcp-pro 的触发条件：需要操作 canvas（`.canvas` 文件）、需要语义搜索（向量化检索）、或不想让 Obsidian 一直开着。

---

## 2. 方案 A：yanxue06/obsidian-mcp（推荐起步）

### 2.1 前置条件

- Obsidian 已安装（见 vault-guide §2）。
- vault 已用 Obsidian 打开（`knowledge/` 文件夹），Obsidian 进程保持运行。

### 2.2 步骤 1：装 Local REST API 插件

yanxue06/obsidian-mcp 不直读文件，而是通过 Obsidian 的 Local REST API 插件暴露的本地 HTTP 端点操作 vault。所以先装这个插件：

1. Obsidian → 设置 → **Community plugins** → **Browse**。
2. 搜索 **Local REST API**（作者 Adam Coddington）→ **Install** → **Enable**。
3. 打开插件设置（插件列表里点齿轮）→ 看到 **API Key** 字段 → **复制**（一长串字符，待会用）。
4. 设置里能看到监听端口（默认 `27124` HTTPS / `27123` HTTP）和证书信息。默认即可。

> API key 是 vault 的写权限凭证，**不要进 git**（见 §5 安全注意事项）。

### 2.3 步骤 2：装 MCP server

在 Claude Code 所在终端跑：

```bash
claude mcp add obsidian \
  -e OBSIDIAN_API_KEY=粘贴你的key \
  -- npx -y @yanxue06/obsidian-mcp
```

参数说明：

- `claude mcp add obsidian`：注册一个名为 `obsidian` 的 MCP server 到 Claude Code。
- `-e OBSIDIAN_API_KEY=...`：把 Local REST API 的 key 作为环境变量传给 server。
- `-- npx -y @yanxue06/obsidian-mcp`：用 npx 拉起 server（首次会下载，`-y` 跳过确认）。

> 包名 `@yanxue06/obsidian-mcp` 以 npm registry 实际发布为准——**待验证**，若拉不到请到 [yanxue06 仓库](https://github.com/yanxue06/obsidian-mcp) 核对最新包名。

### 2.4 步骤 3：验证

1. **完全退出** Claude Code（不是关窗口，是退出进程）。
2. 重新打开 Claude Code。
3. 输入 `/mcp` → 应看到：
   ```
   obsidian ✓ Connected
   ```
4. 在对话里试一句："用 obsidian 列出 vault 里所有 stocks 文件夹的笔记"。若返回笔记列表，连接成功。

### 2.5 步骤 4：常用操作

yanxue06/obsidian-mcp 暴露的工具（具体工具集以仓库 README 为准——**待验证**，下列为典型集）：

| 工具 | 用途 | Claude Code 自然语言用法示例 |
|---|---|---|
| `get_note` | 读取某笔记全文 | "读一下 vault 里 stocks/600519 笔记" |
| `create_note` | 新建/覆盖笔记 | "在 reports/ 下新建一份研报笔记，标题是'茅台三季报点评'" |
| `update_note` | 追加/修改笔记内容 | "在 stocks/600519 的核心业务章节追加一句'2026Q3 营收同比+15%'" |
| `move_note` | 移动/重命名笔记（自动重写反向链接） | "把 stocks/600519 重命名为 stocks/maotai" |
| `delete_note` | 删除笔记（**慎用**，见 §5） | "删掉 stocks/old_test 笔记" |
| `traverse_graph` | 从某笔记出发遍历 N 度双链 | "从 stocks/600519 出发，遍历 2 度关联的所有笔记" |
| `query_dataview` | 跑 DQL 查询返回结果 | "用 dataview 查 vault 里所有 industry 为'食品饮料'的股票" |
| `find_orphans` | 找没有任何双链的孤儿笔记 | "列出 vault 里所有孤儿笔记，我检查下断链" |
| `list_notes` | 列某文件夹下所有笔记 | "列出 strategies 文件夹下所有战法卡" |

> 用法示例是自然语言调用——Claude Code 会自动选对应工具并填参数，你不用记工具名。

### 2.6 故障排除

**ECONNREFUSED（连不上）**

- 原因：Obsidian 没开，或 Local REST API 插件没启用。
- 处理：打开 Obsidian → 确认 vault 已加载 → 设置 → Community plugins → 确认 Local REST API 开关是开的。

**401 Unauthorized**

- 原因：API key 错误或过期。
- 处理：回到 Local REST API 插件设置 → 重新复制 API key → 用 `claude mcp remove obsidian` 删掉旧配置 → 用新 key 重新 `claude mcp add`。

**自签证书警告 / TLS 错误**

- 原因：Local REST API 默认用自签证书，Node 端默认会校验。
- 处理：yanxue06/obsidian-mcp 默认设置 `OBSIDIAN_VERIFY_TLS=false` 跳过校验，正常情况不会报错。若仍报 TLS 错误，显式加环境变量：
  ```bash
  claude mcp add obsidian \
    -e OBSIDIAN_API_KEY=你的key \
    -e OBSIDIAN_VERIFY_TLS=false \
    -- npx -y @yanxue06/obsidian-mcp
  ```

**工具调用超时**

- 原因：vault 太大或 Dataview 查询过重。
- 处理：把大查询拆小，或先在 Obsidian GUI 里跑通 DQL 再丢给 MCP。

---

## 3. 方案 B：obsidian-mcp-pro（升级选项）

### 3.1 适用场景

需要以下任一能力时从 yanxue06 升级到 obsidian-mcp-pro：

- **canvas 操作**：用 AI 创建/修改 `.canvas` 文件（产业链白板、竞争格局图）。
- **语义搜索**：向量化检索"找和茅台业务相似的公司"，不依赖 Smart Connections 插件。
- **无人值守**：不想让 Obsidian 一直开着，agent 也能跑（直读文件系统）。

### 3.2 安装命令

```bash
npx -y obsidian-mcp-pro install \
  --vault /Users/lizhiwei/project/code/stock/Vibe-Research/knowledge
```

> 包名 `obsidian-mcp-pro` 和 install 子命令以项目实际发布为准——**待验证**，安装前到 [obsidian-mcp-pro 仓库](https://github.com/) 核对最新命令。

### 3.3 环境变量配置

obsidian-mcp-pro 直读文件系统，主要环境变量：

| 变量 | 用途 | 示例值 |
|---|---|---|
| `OBSIDIAN_VAULT_PATH` | vault 根路径 | `/Users/lizhiwei/project/code/stock/Vibe-Research/knowledge` |
| `OBSIDIAN_WRITE_PATHS` | 允许写的子路径（白名单） | `stocks/,reports/,analysts/` |
| `OBSIDIAN_READ_ONLY` | 只读模式（禁止任何写操作） | `false` |

注册到 Claude Code：

```bash
claude mcp add obsidian-pro \
  -e OBSIDIAN_VAULT_PATH=/Users/lizhiwei/project/code/stock/Vibe-Research/knowledge \
  -e OBSIDIAN_WRITE_PATHS=stocks/,reports/,analysts/,metrics/,valuations/ \
  -- npx -y obsidian-mcp-pro
```

> 具体变量名以项目 README 为准——**待验证**。

### 3.4 与 yanxue06 的差异说明

| 维度 | yanxue06/obsidian-mcp | obsidian-mcp-pro |
|---|---|---|
| 接入方式 | Local REST API（经 Obsidian） | 直读文件系统 |
| 需要 Obsidian 开着 | 是 | 否 |
| 重命名重写反向链接 | 是（Obsidian 处理） | **待验证**（直读文件系统类实现通常不自动重写） |
| canvas 操作 | 不支持 | 支持 |
| 语义搜索 | 不支持（靠 Smart Connections 插件） | 支持（内置向量化） |
| Dataview 查询 | 支持（直传 Obsidian 跑） | **待验证**（可能需自带 DQL 解析） |
| 风险 | Obsidian 崩了 server 也挂 | 直读文件，并发写有冲突风险 |

> 升级建议：保留 yanxue06 作为日常读写主力（反向链接安全），需要 canvas/语义搜索时临时切 obsidian-mcp-pro。

---

## 4. 与 Vibe-Research MCP 的共存

### 4.1 两套 MCP 各管一摊

Vibe-Research 项目已有一套自研 MCP server（`backend/mcp_server.py`），与本文的 Obsidian MCP 是**两套独立的 MCP server**，各管一摊：

| MCP server | 管什么 | 工具 | 数据来源 |
|---|---|---|---|
| **vibe-research**（`backend/mcp_server.py`） | 实时行情数据 | `query_quote` / `query_valuation` / `query_reports` / `query_news` / `query_global_stock`（另有 `query_strategy_card` / `worldmonitor_query`） | astock / 后端数据库（实时） |
| **obsidian**（本文档配置） | vault 知识层 | `get_note` / `create_note` / `traverse_graph` / `query_dataview` / `find_orphans` 等 | `knowledge/` 文件夹（沉淀知识） |

### 4.2 两者并存

两套 MCP server 可以同时注册到 Claude Code，互不冲突：

```bash
# 已有（Vibe-Research 数据层）
claude mcp add vibe-research -- /路径/backend/.venv/bin/python /路径/backend/mcp_server.py

# 新增（Obsidian 知识层）
claude mcp add obsidian -e OBSIDIAN_API_KEY=你的key -- npx -y @yanxue06/obsidian-mcp
```

`/mcp` 应同时看到两个 ✓ Connected：

```
vibe-research ✓ Connected
obsidian      ✓ Connected
```

### 4.3 组合使用场景示例

> **你**：帮我看下贵州茅台现在估值贵不贵，结合 vault 里沉淀的历史研报观点。

> **AI**（Claude Code，同时调两个 MCP）：
> 1. 调 `vibe-research` 的 `query_valuation` → 拿到当前 PE/PB/PEG/分位（实时数据）。
> 2. 调 `obsidian` 的 `get_note` → 读 `stocks/600519` 笔记里沉淀的核心业务/历史研报摘要。
> 3. 调 `obsidian` 的 `query_dataview` → 跑 `FROM "reports" WHERE contains(code, "600519")` 拿到所有覆盖茅台的研报列表。
> 4. 综合实时估值 + 沉淀观点 → 给出"当前 PE 处于近 5 年 X 分位，研报一致预期目标价 Y，vault 里历史评级买入占比 Z%"这样的回答。

这是 vault 的终极价值：**实时数据（vibe-research MCP）+ 沉淀知识（obsidian MCP）合一**，agent 不只是查数字，还能带上投研上下文。

---

## 5. 安全注意事项

### 5.1 API key 不进 git

Local REST API 的 API key 等同于 vault 的写权限凭证。三个纪律：

1. **不写进任何 `.md` / 配置文件提交到仓库**。`claude mcp add -e` 把 key 存在 Claude Code 的本地配置（通常在 `~/.claude/` 下，不进项目仓库）。
2. **不贴进 commit message / issue / spec**。
3. **轮换**：若怀疑泄露，回 Local REST API 插件设置点 **Regenerate** 生成新 key，旧 key 立即失效。

### 5.2 用 OBSIDIAN_WRITE_PATHS 限制写路径

obsidian-mcp-pro 支持 `OBSIDIAN_WRITE_PATHS` 白名单（见 §3.3），**强烈建议配置**：

```bash
-e OBSIDIAN_WRITE_PATHS=stocks/,reports/,analysts/,metrics/,valuations/,events/,dragon-tiger/
```

只允许 agent 往这些实体文件夹写笔记，**禁止写**：

- `templates/`（模板被改 = 所有新建实体结构被污染）
- `specs/`（项目决策记录，应该人审后再写）
- `data-sources/`（数据源元数据，人维护）
- `MOC.md` / `README.md`（vault 入口，人维护）
- `.obsidian/`（Obsidian 配置，改了可能弄坏插件状态）

> yanxue06/obsidian-mcp 是否支持等价的白名单环境变量 **待验证**——若不支持，写权限管控只能靠 Obsidian 的 Local REST API 插件本身的设置（如果它有路径白名单的话）。

### 5.3 delete_note 慎用

`delete_note` 工具会直接删笔记，且**不会主动清理指向该笔记的 `[[]]` 反向链接**（反向链接会变成"未创建的链接"高亮）。建议：

1. **生产环境禁用**：注册 MCP 时不给 `delete_note` 权限（若 server 支持工具级白名单），或设 `OBSIDIAN_READ_ONLY=true` 只读。
2. **替代方案**：要"删"笔记时，改为 `move_note` 移到 `archive/` 文件夹（保留可恢复），而非真删。
3. **批量清理前先 dry-run**：用 `find_orphans` 列出候选，人工确认后再删——agent 自动批量删笔记风险极高。

### 5.4 vault 备份

接 MCP 前，确保 vault 有备份机制：

- `knowledge/` 已在 git 仓库内 → 定期 `git commit` 是天然快照。
- 大批量自动灌入前，先 `git stash` 或新建分支，灌完验证没问题再合并。

> vault 的 `.gitignore` 已忽略 `.obsidian/` 个人状态，commit 的是纯笔记内容，diff 干净。

---

## 附录：配置自检清单

接完 MCP 后，按此清单过一遍确认全通：

- [ ] Obsidian 已打开 `knowledge/` vault，进程运行中
- [ ] Local REST API 插件已安装并启用
- [ ] Local REST API 的 API key 已复制
- [ ] `claude mcp add` 命令执行成功（用 `claude mcp list` 确认 `obsidian` 在列）
- [ ] Claude Code 完全退出并重开
- [ ] `/mcp` 显示 `obsidian ✓ Connected`
- [ ] 试一句"列出 stocks 文件夹笔记"返回结果
- [ ] `OBSIDIAN_WRITE_PATHS` 白名单已配置（obsidian-mcp-pro）
- [ ] API key 未出现在任何 git tracked 文件中（`git log -p | grep 你的key片段` 应无结果）
- [ ] vibe-research MCP 仍正常（`/mcp` 两个都 ✓）
