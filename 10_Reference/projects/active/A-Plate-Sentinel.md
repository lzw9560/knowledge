
# A-Plate-Sentinel

## 项目概述
A 股板块情绪监控工具。定时扫描板块涨跌幅/资金流向/涨停家数，输出情绪仪表盘。与 Vibe-Research 互补——Vibe-Research 是单点投研助理，A-Plate-Sentinel 是全市场情绪扫描。

详细实体笔记在投研子区：H_Reference/investing/specs/a-Plate-Sentinel项目|a-Plate-Sentinel 项目实体]]。

## 技术栈
- 语言：[[10_Reference/tech-learning/languages/python|Python]]
- 容器化：H_Reference/tech-learning/tools/Docker|Docker]] / Docker Compose 本地部署
- 数据源：与 H_Reference/projects/active/Vibe-Research|Vibe-Research]] 共享（H_Reference/investing/data-sources/AkShare|akshare]] / H_Reference/investing/data-sources/东财 push2|东财]] 等）

## 与 Vibe-Research 的关系
- 定位差异：Vibe-Research = 单点深查，A-Plate-Sentinel = 全市场广扫
- 数据共享：共用 4 数据源（mootdx / 东财 / 新浪 / 同花顺）
- 情绪互通：A-Plate-Sentinel 的板块情绪可喂给 Vibe-Research 的 H_Reference/market_sentiment/情绪仪表盘|市场情绪看板]]

## 相关链接
- [[10_Reference/projects/MOC]]
- [[10_Reference/investing/MOC]]
- H_Reference/investing/specs/a-Plate-Sentinel项目]]
- [[10_Reference/tech-learning/MOC]]
- H_Reference/projects/active/Vibe-Research]]
- H_Reference/meta/四构件本体方法论]]
