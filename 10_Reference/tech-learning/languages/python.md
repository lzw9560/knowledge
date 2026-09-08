---
type: language
name: Python
paradigm: 多范式（面向对象/函数式/过程式）
typing: 动态类型（duck typing，可选 type hints + mypy 静态检查）
created: 2026-09-07
---

# Python

## 范式
- 多范式：面向对象、函数式、过程式皆可
- 解释执行（CPython），JIT 变体（PyPy）
- 显式优于隐式（PEP 20 / The Zen of Python）

## 类型系统
- 动态类型 + 鸭子类型
- PEP 484 type hints（可选，配合 mypy/pyright 做静态检查）
- Pydantic / dataclasses 做运行时结构化校验

## 主要应用领域
- 数据科学 / 机器学习（NumPy/Pandas/PyTorch/scikit-learn）
- 后端 Web（FastAPI/Django/Flask）
- 自动化脚本 / DevOps（Ansible/_salt_）
- 投研数据管道（akshare/tushare/pandas）

## 在 Vibe-Research 中的使用
- 后端主语言：[[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移|S008]] 数据层用 Pydantic 契约模型
- 数据源接入：[[10_Reference/investing/data-sources/AkShare|AkShare]][[akshare]] / mootdx / 东财均用 Python SDK
- 战法执行：[[10_Reference/investing/strategies/|战法卡]] 在 `backend/strategies/cards/` 实现
- 配套框架：[[10_Reference/[[tech-learning/frameworks/fastapi]]

## 相关链接
- [[10_Reference/[[tech-learning/MOC]]
- [[10_Reference/[[tech-learning/frameworks/fastapi]]
- [[10_Reference/investing/MOC]]
- [[10_Reference/investing/data-sources/AkShare]]
- [[10_Reference/investing/specs/archive/m0-foundation/S008-后端数据层迁移]]
- [[10_Reference/[[meta/四构件本体方法论]]
