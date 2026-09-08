---
type: tool
name: uv
category: Python 包管理器
created: 2026-09-07
---

# uv

## 类别
- Python 包管理器 + 虚拟环境管理器（Rust 实现，Astral 出品）
- 集成 pip / pip-tools / virtualenv / pipx / poetry 多工具于一身
- 与 pip / poetry 的对比：uv 是 pip 的 10-100x 速度替代，无需切换心智模型

## 核心用途
- **依赖安装**：`uv pip install` 比 pip 快 10-100x（Rust 实现 + 全局缓存）
- **虚拟环境**：`uv venv` 创建，自动管理 `.venv`
- **依赖锁定**：`uv lock` 生成 `uv.lock`，可复现安装
- **项目同步**：`uv sync` 一键安装项目依赖到当前环境
- **Python 版本管理**：`uv python install 3.12` 自带 Python 版本下载（替代 pyenv）

## 在 Vibe-Research 中的使用
- Python 依赖管理：`backend/` 用 `pyproject.toml` + `uv.lock`
- 投研数据源 SDK 安装：[[10_Reference/investing/data-sources/akshare|akshare]] / mootdx 等 Python 包由 uv 统一管理与锁版本
- 与 [[10_Reference/tech-learning/tools/docker|Docker]] 配合：Dockerfile 中用 `uv sync --frozen` 做可复现构建
- 与 [[10_Reference/tech-learning/frameworks/pydantic|Pydantic]] / [[10_Reference/tech-learning/frameworks/fastapi|FastAPI]] 配合：uv 管理这些依赖的安装与锁版本

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- [[10_Reference/tech-learning/languages/python]]
- [[10_Reference/tech-learning/tools/docker]]
- [[10_Reference/tech-learning/frameworks/pydantic]]
- [[10_Reference/tech-learning/frameworks/fastapi]]
- [[10_Reference/meta/four-construct-ontology]]
