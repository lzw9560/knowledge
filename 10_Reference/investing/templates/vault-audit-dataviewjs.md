---
type: audit
audit_date: <% tp.date.now("YYYY-MM-DD") %>
auditor: obsidian-dataviewjs
scope: 全量
findings_count: 0
critical: 0
high: 0
medium: 0
low: 0
status: 自动审查
created: <% tp.date.now("YYYY-MM-DD") %>
---

# 审查报告：<% tp.date.now("YYYY-MM-DD") %>（Obsidian 自动）

> 由 DataviewJS 自动生成。8 项检查。
> 报告位置：`10_Reference/investing/reviews/`，文件名 `YYYY-MM-DD-obsidian-audit.md`。
> frontmatter 计数字段保持 0（DataviewJS 渲染时不回写文件），机器可判计数见下方"问题清单"区。

## 1. summary（图谱摘要）

```dataviewjs
const base = "10_Reference/investing";
const folders = ["stocks","industries","concepts","indices","reports","analysts","metrics","valuations","dragon-tiger","events","strategies","specs","data-sources","logic","actions","inbox","reviews"];
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const totalLinks = all.reduce((sum, p) => sum + p.file.outlinks.length, 0);
dv.paragraph("**实体笔记总数**：" + all.length + " ｜ **关系总数（出边累计）**：" + totalLinks + " ｜ **审查范围**：全量（排除 templates/）");
const rows = folders.map(f => {
  const n = dv.pages('"' + base + "/" + f + '"').where(p => !p.file.path.includes("/templates/")).length;
  return [f, n];
});
dv.table(["文件夹", "笔记数"], rows);
```

## 2. coverage（覆盖率）

```dataviewjs
const base = "10_Reference/investing";
const folders = ["stocks","industries","concepts","indices","reports","analysts","metrics","valuations","dragon-tiger","events","strategies","specs","data-sources","logic","actions","inbox","reviews"];
let zeros = [];
let lows = [];
const rows = folders.map(f => {
  const n = dv.pages('"' + base + "/" + f + '"').where(p => !p.file.path.includes("/templates/")).length;
  const status = n === 0 ? "❌ 空" : (n < 3 ? "⚠️ 偏少" : "✓");
  if (n === 0) zeros.push(f);
  if (n > 0 && n < 3) lows.push(f);
  return [f, n, status];
});
dv.table(["文件夹", "笔记数", "状态"], rows);
if (zeros.length > 0) {
  dv.paragraph("**⚠️ 空文件夹（" + zeros.length + "）**：" + zeros.join("、") + " — 建议至少补一个 index.md 导航。");
}
if (lows.length > 0) {
  dv.paragraph("**⚠️ 偏少文件夹（" + lows.length + "）**：" + lows.join("、") + " — 数量 <3，确认是否待导入。");
}
if (zeros.length === 0 && lows.length === 0) {
  dv.paragraph("**✓ 覆盖正常**：所有文件夹均有 ≥3 条笔记。");
}
```

## 3. orphan_check（孤立实体）

```dataviewjs
const base = "10_Reference/investing";
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const orphans = all.where(p => p.file.inlinks.length === 0)
  .sort(p => p.file.path);
dv.paragraph("**无入边实体数**：" + orphans.length);
if (orphans.length === 0) {
  dv.paragraph("✓ 无孤立实体。");
} else {
  dv.table(["文件", "路径", "类型"], orphans.map(p => [p.file.link, p.file.folder, p.type || "—"]));
}
```

## 4. broken_link（断链）

```dataviewjs
const base = "10_Reference/investing";
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const norm = (s) => String(s).replace(/\.md$/, "").toLowerCase();
const allPaths = new Set(all.map(p => norm(p.file.path)));
const broken = [];
for (const p of all) {
  for (const link of p.file.outlinks) {
    if (!allPaths.has(norm(link.path))) {
      broken.push([p.file.link, link.path, link.display || link.path]);
    }
  }
}
dv.paragraph("**断链数**：" + broken.length);
if (broken.length === 0) {
  dv.paragraph("✓ 无断链。");
} else {
  dv.table(["源文件", "断链目标", "显示文本"], broken);
}
```

## 5. schema_infer（schema 偏差）

```dataviewjs
const base = "10_Reference/investing";
// 设计模板字段（蒸馏自 templates/*.md，含 type 与 created）
const expected = {
  stock:        ["type","code","name","market","industry","concept","list_date","st","pe_ttm","pb","market_cap","created"],
  industry:     ["type","code","name","source","created"],
  concept:      ["type","code","name","related_industry","created"],
  index:        ["type","code","name","market","created"],
  report:       ["type","code","title","org","researcher","publish_date","report_type","rating_change","target_price","eps_forecast","created"],
  analyst:      ["type","name","org","coverage_count","created"],
  metric:       ["type","code","period","revenue","net_profit","roe","gross_margin","net_margin","eps","bvps","op_cf_ps","created"],
  valuation:    ["type","code","pe_ttm","pb","ps_ttm","pcf_ttm","dividend_yield","peg","forward_pe","consensus_eps","pe_percentile","pb_percentile","created"],
  dragon_tiger: ["type","code","date","institution_net","seats","created"],
  event:        ["type","date","event_type","codes","source","summary","created"],
  strategy:     ["type","name","edge_family","match_conditions","entry_conditions","exit_conditions","created"],
  spec:         ["type","number","title","status","created"],
  data_source:  ["type","name","layer","endpoint","rate_limit","fallback","created"],
  logic:        ["type","rule_id","rule_type","target_entity","severity","condition","action_on_violation","source","created"],
  action:       ["type","action_id","action_type","trigger","target","audit","created"],
  inbox_item:   ["type","entity_type","name","code","confidence","source","quality_score","completeness","consistency","linkage","traceability","approved","approved_date","rejected","reject_reason","created"]
};
const required = { // 必填字段（缺失算 high）
  stock: ["code","name"], industry: ["code","name"], concept: ["code","name"],
  index: ["code","name"], report: ["code","title"], analyst: ["name"],
  metric: ["code","period"], valuation: ["code"], dragon_tiger: ["code","date"],
  event: ["date","event_type"], strategy: ["name"], spec: ["number","title"],
  data_source: ["name"], logic: ["rule_id"], action: ["action_id"], inbox_item: ["name"]
};
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const deviations = [];
const missing = [];
for (const p of all) {
  const t = p.type;
  if (!t || !expected[t]) continue;
  const exp = expected[t];
  const actual = Object.keys(p.file.frontmatter || {});
  const extra = actual.filter(k => !exp.includes(k));
  const miss = (required[t] || []).filter(k => !(p.file.frontmatter && p.file.frontmatter[k] !== undefined && p.file.frontmatter[k] !== ""));
  if (extra.length > 0) deviations.push([p.file.link, t, extra.join(", "), ""]);
  if (miss.length > 0) missing.push([p.file.link, t, miss.join(", ")]);
}
dv.paragraph("**新增字段（实际有、设计无）**：" + deviations.length + " ｜ **缺失必填**：" + missing.length);
if (deviations.length > 0) dv.table(["文件","类型","新增字段",""], deviations);
if (missing.length > 0) dv.table(["文件","类型","缺失必填",""], missing);
if (deviations.length === 0 && missing.length === 0) dv.paragraph("✓ 无 schema 偏差。");
```

## 6. relation_density（关系密度）

```dataviewjs
const base = "10_Reference/investing";
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const HUB_THRESHOLD = 10;
const density = all.map(p => ({
  link: p.file.link,
  type: p.type || "—",
  inlinks: p.file.inlinks.length,
  outlinks: p.file.outlinks.length
}));
const hubs = density.filter(d => d.inlinks >= HUB_THRESHOLD).sort((a,b) => b.inlinks - a.inlinks);
const islands = density.filter(d => d.inlinks === 0 && d.outlinks === 0);
dv.paragraph("**入边 ≥ " + HUB_THRESHOLD + " 的 hub**：" + hubs.length + " ｜ **完全孤立（0 入 0 出）**：" + islands.length);
if (hubs.length > 0) {
  dv.paragraph("**⚠️ Hub 风险（入边过多，拆分风险）**：");
  dv.table(["文件","类型","入边数","出边数"], hubs.map(d => [d.link, d.type, d.inlinks, d.outlinks]));
}
if (islands.length > 0) {
  dv.paragraph("**⚠️ 信息孤岛（0 入 0 出）**：");
  dv.table(["文件","类型","入边数","出边数"], islands.map(d => [d.link, d.type, d.inlinks, d.outlinks]));
}
if (hubs.length === 0 && islands.length === 0) dv.paragraph("✓ 关系密度正常。");
```

## 7. duplicate_check（重复）

```dataviewjs
const base = "10_Reference/investing";
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const groupBy = (keyFn) => {
  const m = {};
  for (const p of all) {
    const k = keyFn(p);
    if (k === undefined || k === null || k === "") continue;
    const sk = String(k);
    if (!m[sk]) m[sk] = [];
    m[sk].push(p);
  }
  return Object.entries(m).filter(([k, ps]) => ps.length > 1)
    .map(([k, ps]) => [k, ps.length, ps.map(p => p.file.link).join(" | ")]);
};
const dupCode = groupBy(p => p.code);
const dupName = groupBy(p => p.name);
dv.paragraph("**同 code 重复**：" + dupCode.length + " ｜ **同 name 重复**：" + dupName.length);
if (dupCode.length > 0) {
  dv.paragraph("**⚠️ 同代码多记录**：");
  dv.table(["代码","记录数","文件"], dupCode);
}
if (dupName.length > 0) {
  dv.paragraph("**⚠️ 同名称多记录**：");
  dv.table(["名称","记录数","文件"], dupName);
}
if (dupCode.length === 0 && dupName.length === 0) dv.paragraph("✓ 无重复实体。");
```

## 8. stale_check（过期）

```dataviewjs
const base = "10_Reference/investing";
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const now = Date.now();
const STALE_DAYS = 90;
const STALE_MS = STALE_DAYS * 24 * 3600 * 1000;
const stale = all.filter(p => p.file.mtime && (now - p.file.mtime.toMillis()) > STALE_MS)
  .sort((a,b) => a.file.mtime.toMillis() - b.file.mtime.toMillis())
  .map(p => {
    const days = Math.floor((now - p.file.mtime.toMillis()) / 86400000);
    return [p.file.link, p.file.folder, p.file.mtime.toFormat("yyyy-MM-dd"), days];
  });
dv.paragraph("**超 " + STALE_DAYS + " 天未更新**：" + stale.length);
if (stale.length === 0) {
  dv.paragraph("✓ 无过期实体。");
} else {
  dv.table(["文件","路径","最后修改","距今天数"], stale);
}
```

## 问题清单

> 机器可判定的级别统计（重新扫描 orphan / broken / stale / duplicate）。
> schema 偏差与 relation_density 的级别判定见上各节，人工复核后补入下表。

```dataviewjs
const base = "10_Reference/investing";
const all = dv.pages('"' + base + '"').where(p => !p.file.path.includes("/templates/"));
const norm = (s) => String(s).replace(/\.md$/, "").toLowerCase();
const allPaths = new Set(all.map(p => norm(p.file.path)));
let critical = 0, high = 0, medium = 0, low = 0;
// broken_link → critical
let broken = 0;
for (const p of all) {
  for (const link of p.file.outlinks) {
    if (!allPaths.has(norm(link.path))) broken++;
  }
}
critical += broken;
// orphan → high（核心实体孤立）
const orphans = all.where(p => p.file.inlinks.length === 0).length;
high += orphans;
// duplicate → medium
const byCode = {};
for (const p of all) {
  if (p.code) {
    const k = String(p.code);
    if (!byCode[k]) byCode[k] = 0;
    byCode[k]++;
  }
}
const dup = Object.values(byCode).filter(n => n > 1).length;
medium += dup;
// stale → low
const now = Date.now();
const STALE_MS = 90 * 24 * 3600 * 1000;
const stale = all.filter(p => p.file.mtime && (now - p.file.mtime.toMillis()) > STALE_MS).length;
low += stale;
dv.table(["级别","计数","判定来源"], [
  ["Critical（阻断）", critical, "断链"],
  ["High（优先修）", high, "孤立实体"],
  ["Medium（进 backlog）", medium, "重复实体"],
  ["Low（知悉即可）", low, "90 天未更新"]
]);
dv.paragraph("**合计**：" + (critical + high + medium + low) + " ｜ 提示：frontmatter 计数字段保持 0，以本表为准。");
```

### Critical（阻断）

- 见上 broken_link 节，逐条修复断链目标。

### High（优先修）

- 见上 orphan_check 节，给孤立实体补入边（被引用）或确认是否应删除。

### Medium（进 backlog）

- 见上 duplicate_check 节，合并同 code/name 的重复记录。

### Low（知悉即可）

- 见上 stale_check 节，确认过期实体是否仍有效。

## 修复建议

1. **断链（Critical）**：逐条检查 broken_link 表，目标不存在则创建或改链接。
2. **孤立实体（High）**：从相关行业/概念/战法笔记补 `[[]]` 入边；确认 inbox 未审实体。
3. **重复（Medium）**：同 code 合并为一条，其余改别名或删除。
4. **过期（Low）**：超 90 天未更新的，确认数据是否过时，过时则更新或标注 `stale: true`。
5. **schema 偏差**：新增字段若通用，反向更新 `templates/` 对应模板；缺失必填则补值。

## 跟踪

- [ ] Critical 全部修复
- [ ] High 修复或进 spec
- [ ] Medium 进 backlog
- [ ] 下次审查日期：
