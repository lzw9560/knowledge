---
type: tool
name: Docker
category: 容器化 / DevOps
created: 2026-09-07
---

# Docker

## 类别
- 容器化运行时
- 配套：Docker Compose（多容器编排）/ Dockerfile（镜像构建）

## 核心用途
- 环境隔离：Python/Node/DB 各自独立运行时
- 可复现部署：image 即"打包的运行环境"
- 跨机器一致：开发机 = 生产机配置
- 与 K8s 的差异：Docker Compose 是单机编排，K8s 是多机集群编排

## 在 Vibe-Research 中的使用
- 本地开发：`docker-compose.yml` 起 backend + frontend + DB
- 关联项目 a-Plate-Sentinel 也用 Docker Compose 本地部署（见 10_Reference/investing/specs/a-Plate-Sentinel项目|a-Plate-Sentinel]]）

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/investing/MOC]]
- 10_Reference/investing/specs/a-Plate-Sentinel项目]]
- 10_Reference/meta/四构件本体方法论]]
