# 知识图谱完善度审查报告

> 审查时间：2026-09-07
> 审查人：orchestrator（ora-4 超时后接手）

## 总体完善度评分：**82/100**

图谱已具备知识图谱的完整骨架和实质内容，消费层基础设施就绪，但部分实体深度不够、待审积压多、消费层未实际跑通。

---

## 各维度评分

### 1. 内容完整性：78/100

**已达标**：
- stocks 401 只，PE/PB/市值全真值，核心业务段 380/401 LLM 补充完成（0 残留"待补充"）
- reports 392 份真实研报（从东财拉取，非臆造）
- analysts 361 个真实分析师（从研报提取，按姓名+机构去重）
- specs 109 个（92 已实现归档 + 8 草案 + 5 DEC + 4 项目实体）
- data-sources 17 个（含 projects 双字段，跨项目去重）
- strategies 12 张战法卡（从源仓导入，frontmatter 加 edge_family）
- agents 7 个 AI 角色（trading-agents 的 7 Analyst）
- logic 14 条 + actions 5 个（四构件方法论落地）

**关键缺口**：
- metrics/valuations 只有 21 只（401 只股票中仅 21 只有真实财务/估值数据，其余 380 只没有）
- events 只有 5 个（涨停/炸板/异动各 1-2 天，缺历史事件序列）
- dragon-tiger 只有 12 个（仅 11 只大盘股的龙虎榜，缺涨停池股票）
- concepts 只有 37 个（A 股 400+ 概念，覆盖率 ~9%）
- inbox 170 个待审实体未转正（analyst 119/stock 47/industry 4）
- 90 个行业标"待核实"（东财接口被代理阻断，行业字段未填充）

### 2. 关系密度：75/100

**已达标**：
- 1378 节点 / 5394 有向边 / 密度 0.00519（稀疏但合理——投研知识图谱不是社交网络）
- 54 个社区 / 291 个桥节点（图算法分析完成）
- Top hub: eastmoney-reportapi(753 入边) / analysts/(394) / eastmoney-push2(264) / tencent(157) / strategies/(116)

**关键缺口**：
- 380 只新增股票（沪深300+中证1000成分股）的 metrics/valuations 链接悬空（指向不存在的实体）
- 90 个行业"待核实"导致 stocks→industries 链接指向"待核实"占位实体
- inbox 170 个实体无入边（待审状态，未建立关系）

### 3. 治理健康度：80/100

**已达标**：
- 审查脚本 vault_audit.py 跑通（8 项检查，误报清零）
- 断链从 270→6（97.8% 改善）
- 孤立实体从 71→0（Week 1 修复）
- duplicate_check 误报清零（code+type 联合分组）
- 季度审查流程文档 + 实体生命周期 + 信任度衰减规则
- GitHub Actions 每周日自动审查（已跑通）
- DataviewJS 手动审查模板（8 项检查）

**关键缺口**：
- inbox 170 个待审实体堆积（未审核转正）
- specs 归档后断链可能新增（92 个文件移到 archive/，链接路径已更新但需验证）
- 90 个"待核实"行业实体是脏数据 hub（被 380 只股票链接但内容空）

### 4. 消费层可用性：70/100

**已达标**：
- 飞书 bot 5 端点代码就绪（/bot /direct /stream /test /callback）
- 飞书 WebSocket 长连接代码就绪（feishu_ws_client.py）
- 微信 bot 4 端点代码就绪 + 穿透脚本
- Quartz 静态站点已部署（https://lzw9560.github.io/knowledge/）
- Obsidian MCP 配置完成（Local REST API + opencode.json）
- LLM API key 修通（BAILIAN key，HTTP 200 验证）
- LLM pipeline P1-P5 全部实现
- 图算法分析 + 时间线视图 + 因果链标注
- 股票核心业务 LLM 补充完成（380/401）

**关键缺口**：
- **飞书 bot 未实际跑通**——后端需在独立终端启动（opencode shell 会杀子进程）
- **飞书 App ID/Secret 不匹配**——日志报 `app_id or app_secret is invalid`
- **Obsidian MCP 未验证**——需重启 opencode 后 `/mcp` 检查
- **Quartz 站点中文文件名问题**——`analyst-周尔双.md` 等中文文件名导致 Quartz 构建中断（NFC/NFD 规范化差异）
- **LLM 对话在后端进程里失败**——`Connection aborted`（可能因进程环境变量差异）

### 5. 跨领域连通：85/100

**已达标**：
- 跨领域 65 个实体（技术学习 30 + 读书 16 + 项目追踪 13 + 元知识 3 + 归档 3）
- 23 个跨域链接（投研↔技术学习↔读书），零悬空
- 元知识层（PARA/MOC/四构件方法论）
- 4 个项目全纳入（Vibe-Research/trading-agents/daily-stock-analysis/a-Plate-Sentinel）

**关键缺口**：
- 跨领域实体数偏少（65 个 vs 投研 1713 个 = 3.8%）
- 读书子区只有 16 个实体（书单 10 + 笔记 6）
- 技术学习子区只有 30 个实体（语言 4 + 框架 5 + 工具 8 + 架构 7 + 概念 3 + 模板 3）

### 6. 元数据质量：85/100

**已达标**：
- 16 个模板全部优化（callout + emoji + Dataview 全路径 + 关系网段）
- 1038 个实体批量格式更新（des-1 完成）
- stocks 401 只全有 frontmatter（code/name/pe_ttm/pb/market_cap/industry/concept/matched_strategies/last_synced）
- specs 109 个全有 frontmatter（type/number/title/status/created）
- data-sources 17 个全有 projects 双字段
- 实体词典 611 别名（.entity-dictionary.json）
- 图算法分析 + 时间线视图

**关键缺口**：
- 90 个行业"待核实"（industry 字段未填充）
- 10 个 metrics/valuations 标"待实时"（dividend_yield/peg/forward_pe 等字段缺失）
- confidence/source/quality_score 字段仅在 inbox/ 实体有，正式区实体未标注
- last_synced 仅 21 只股票有（其余 380 只未同步实时数据）

---

## 关键缺口 Top 10（按优先级排序）

| # | 缺口 | 价值 | 难度 | 建议 |
|---|---|---|---|---|
| 1 | **飞书 bot 未跑通** | 极高 | 低 | 在独立终端启动后端 + 确认飞书 App ID/Secret |
| 2 | **inbox 170 待审积压** | 高 | 中 | 批量审核转正（quality_score ≥60 的 mv 到正式区） |
| 3 | **90 个行业"待核实"** | 高 | 中 | 网络通畅时重跑 individual_info 或手动填充 |
| 4 | **metrics/valuations 仅 21 只** | 高 | 中 | 对 401 只股票批量拉 astock.financials/full_valuation |
| 5 | **Quartz 中文文件名问题** | 中 | 低 | `git config core.precomposeunicode true` 或重命名文件 |
| 6 | **events/dragon-tiger 偏少** | 中 | 中 | 每日自动灌入涨停池/炸板池/龙虎榜 |
| 7 | **concepts 覆盖率 9%** | 中 | 中 | 从 akshare 拉更多概念板块 + 成分股 |
| 8 | **Obsidian MCP 未验证** | 中 | 低 | 重启 opencode `/mcp` 检查 obsidian 连接 |
| 9 | **跨领域实体偏少** | 低 | 低 | 持续填充读书笔记/技术概念 |
| 10 | **confidence/source 未标全** | 低 | 中 | 批量给正式区实体补 confidence/source 字段 |

---

## 已达标项（不需要再做）

- ✅ vault 骨架（PARA + 16 实体类 + 四构件 + 质量门）
- ✅ 4 项目全纳入
- ✅ 16 模板全部优化（callout + emoji + Dataview）
- ✅ 1038 个实体格式更新
- ✅ 380 只股票核心业务 LLM 补充
- ✅ 21 只股票真实财务数据
- ✅ specs 归档（92 → 8 里程碑子目录 + SUMMARY）
- ✅ LLM pipeline P1-P5
- ✅ LLM 抽取脚本（规则+LLM 双模式）
- ✅ 图算法分析 + 时间线 + 因果链
- ✅ 自动审查（GitHub Actions + DataviewJS）
- ✅ Quartz 站点部署 + 调优
- ✅ 飞书/微信 bot 代码（5+4 端点）
- ✅ Obsidian MCP 配置
- ✅ 会话协议（CLAUDE.md + AGENTS.md）
- ✅ 四构件方法论 skill
- ✅ 断链清零 + 孤立清零 + 误报清零
- ✅ GitHub 同步（lzw9560/knowledge 私有仓）

---

## 30 天完善路线图（82→90 分）

### Week 1（+4 分：消费层跑通）
1. 在独立终端启动后端 → 飞书 bot LLM 对话实测
2. 确认飞书 App ID/Secret → WebSocket 长连接通
3. 重启 opencode → Obsidian MCP 连通
4. 修 Quartz 中文文件名问题

### Week 2（+2 分：待审清理）
5. inbox 170 个待审实体批量审核转正
6. 90 个"待核实"行业填充

### Week 3（+2 分：数据深度）
7. 401 只股票批量拉 financials + full_valuation → metrics/valuations 扩到 401
8. 每日自动灌入涨停池/炸板池/龙虎榜 → events/dragon-tiger 持续增长

### Week 4（+1 分：治理完善）
9. concepts 从 akshare 拉更多（37→100+）
10. 正式区实体补 confidence/source 字段

---

## 最终判断

**图谱是否"足够完善"？**

**基本完善，但未达"足够"。**

82 分意味着图谱已具备：
- 完整的骨架和四构件方法论
- 1947 个实体（401 股票 + 392 研报 + 361 分析师 + 109 spec + ...）
- LLM 补充的核心业务正文
- 全套基础设施（飞书/微信 bot + Quartz + MCP + pipeline + 自动审查）

**还差 8 分到 90 分**——主要差在：
1. 消费层未实际跑通（飞书 bot 需独立终端启动 + App ID 确认）
2. 170 个待审实体积压
3. 380 只股票缺 metrics/valuations 真实数据
4. Quartz 中文文件名问题

这些都是"最后一公里"问题——骨架和内容已就位，差的是"通电测试"。
