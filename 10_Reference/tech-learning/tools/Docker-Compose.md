---
type: tool
name: Docker Compose
category: 容器编排
created: 2026-09-07
---

# Docker Compose

## 类别
- 多容器编排工具（Docker 官方）
- 与单容器 [[10_Reference/[[tech-learning/tools/Docker|Docker]][[Docker]] 互补：Docker 管"一个容器怎么跑"，Compose 管"多个容器怎么一起跑"

## 核心特性
- **声明式配置**：`docker-compose.yml` 描述服务/网络/卷
- **一键启停**：`docker compose up -d` / `docker compose down`
- **依赖编排**：`depends_on` 控制启动顺序（如 db 先于 api）
- **环境隔离**：每个 compose project 独立网络与卷
- **配置复用**：`docker-compose.override.yml` 覆盖本地开发配置

## 常用命令
- `docker compose up -d` — 后台启动全部服务
- `docker compose ps` — 查看服务状态
- `docker compose logs -f <service>` — 跟踪日志
- `docker compose restart <service>` — 重启单服务
- `docker compose build` — 重建镜像
- `docker compose down -v` — 停止并删卷（**慎用，数据卷会丢**）

## 典型多容器拓扑
```yaml
services:
  db:        # 数据层
  redis:     # 缓存/事件总线
  api:       # 后端 FastAPI
  web:       # 前端 Vite/React
  scheduler: # 调度器（独立进程）
```

## 在 Vibe-Research 生态中的使用
- [[10_Reference/[[projects/active/A-Plate-Sentinel|a-Plate-]][[Sentinel]] — 板块情绪哨兵，多容器编排（scrapy + redis + api）
- [[10_Reference/[[projects/active/Vibe-Research|Vibe-]][[Research]] — 本仓的 docker-compose 用于本地起 db + redis + api
- 与 [[10_Reference/[[tech-learning/architecture/微服务架构|微服务架构]][[微服务]] 架构天然搭配：Compose 是开发态微服务编排的最小可行工具

## 相关链接
- [[10_Reference/[[tech-learning/MOC]]
- [[10_Reference/[[tech-learning/tools/Docker]]
- [[10_Reference/[[tech-learning/architecture/微服务架构]]
- [[10_Reference/[[projects/active/A-Plate-Sentinel]]
- [[10_Reference/[[meta/四构件本体方法论]]
