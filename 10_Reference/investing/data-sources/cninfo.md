---
type: data_source
name: 巨潮 cninfo（互动易）
layer: 4
endpoint: www.cninfo.com.cn
rate_limit: requests 直连
fallback: 无
compliance: ok
provides: [公告, 互动易问答]
created: 2026-09-06
---

# 巨潮 cninfo（互动易）

## 提供字段
- 公告
- 互动易问答

## 限流策略
- requests 直连
- 待补：具体限流策略（未在 ARCHITECTURE.md 明示封禁行为）

## 降级链
- 无

## 相关实体
- 喂给实体类型：[[news/]] [[events/]] [[stocks/]]
- 对应代码：`backend/data/sources/astock.py`（待补：具体函数名）

## 相关 spec
- [[specs/]] 后端数据层迁移 / 公告接入
