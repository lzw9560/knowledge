---
type: data_source
name: 108 RSS 源（资讯雷达）
layer: 资讯层
endpoint: 108 源
rate_limit: 40线程并发
fallback: 单源失败不拖垮整体
compliance: ok
provides: [资讯, 12赛道分类, 合规过滤]
created: 2026-09-06
last_synced: 2026-09-07
---

# 108 RSS 源（资讯雷达）

## 提供字段
- 资讯条目（标题/时间/来源/正文）
- 12 赛道分类
- 合规词表过滤（赌/预测市场/加密/色情命中即跳过）

## 限流策略
- `ThreadPoolExecutor(40)` 并发
- 单源失败不拖垮整体

## 降级链
- 单源失败 → 跳过该源，不影响整体
- 缓存原子写（tmp + `os.replace`）
- `force` 参数强制刷新

## 相关实体
- 喂给实体类型：[[events/]]
- 对应代码：`backend/data/sources/newsradar.py` → `fetch_radar`、`get_radar(force)`
- 缓存：`backend/.cache/radar.json`

## 相关 spec
- [[specs/]] 资讯雷达接入 / 12 赛道 / 合规词表

<!-- pipeline: P4 extract_relations.py 生成 -->

## 数据流关系

**关联 spec**：
- [[specs/S020-worldmonitor决策因子接入]]（S020）
