---
type: concept
name: 熔断器
category: 编程概念
created: 2026-09-07
---

# 熔断器（Circuit Breaker）

## 类别
- 容错模式（Michael Nygard 《Release It!》2007 提出）
- 多语言实现：Python（`pybreaker`/`circuitbreaker`）、Java（Resilience4j/Hystrix）、TS（opossum）

## 核心特性
- **三状态机**：关闭（Closed）→ 打开（Open）→ 半开（Half-Open）→ 关闭/打开
  - Closed：请求正常通过，统计失败率
  - Open：失败率超阈值，直接拒绝请求（快速失败），等待 cooldown
  - Half-Open：cooldown 后放行少量请求探测，成功则回 Closed，失败则回 Open
- **滑动窗口统计**：基于时间窗口或请求数窗口统计失败率
- **快速失败**：Open 状态不调下游，直接返回 fallback——保护下游 + 释放上游资源
- **降级**：熔断时返回兜底值（缓存/默认值），而非报错

## 状态机示意
```
  Closed ──(失败率>阈值)──> Open
    ▲                          │
    │                     (cooldown 后)
    │                          ▼
    └──(探测成功)──────── Half-Open
                               │
                          (探测失败)
                               ▼
                             Open
```

## 在 Vibe-Research 中的使用
- [[10_Reference/investing/specs/S022-em_get-防封熔断|S022 em_get 防封熔断]] — em_get 调用加熔断，连续失败快速失败避免触发更严风控
- [[10_Reference/investing/strategies/storm_reversal|暴风雨反转战法]] — 名字类比：股市"急跌反弹"即市场级"熔断后 Half-Open 探测"
- [[10_Reference/tech-learning/concepts/caching-strategy|缓存策略]] — 降级 fallback 常用缓存值

## 与投研"天气熔断"的类比
- A 股的"涨跌停板"即市场级熔断：单日价格波动超 ±10% 即触发
- 战法卡的"适用天气：阴天/晴天"判据即策略级熔断：市场异常时停止开仓

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/tech-learning/concepts/caching-strategy]]
- [[10_Reference/investing/specs/S022-em_get-防封熔断]]
- [[10_Reference/investing/strategies/storm_reversal]]
- [[10_Reference/meta/four-construct-ontology]]
