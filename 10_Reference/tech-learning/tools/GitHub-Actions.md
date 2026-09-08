---
type: tool
name: GitHub Actions
category: CI/CD
created: 2026-09-07
---

# GitHub Actions

## 类别
- GitHub 原生 CI/CD 平台
- 与 10_Reference/tech-learning/tools/Git|Git]] 同源：commit/push 即触发

## 核心特性
- **YAML 声明式**：`.github/workflows/*.yml` 定义流水线
- **触发器**：`push` / `pull_request` / `schedule`（cron）/ `workflow_dispatch`（手动）
- **矩阵构建**：`matrix` 跨 OS / runtime / 版本并行
- **复用**：`workflow_call` 复合工作流 / `actions/` 市场复用 step
- **Secrets**：仓库级 / 环境级加密变量

## 常用工作流模式
```yaml
on:
  push:
    branches: [develop]
  schedule:
    - cron: "0 1 * * 1-5"  # 工作日凌晨 1 点
jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      - run: pytest
```

## 在 Vibe-Research 生态中的使用
- **vault-audit workflow**：本知识图谱 vault 的自动审计（链接有效性扫描、孤立实体检测）
- **quartz-deploy workflow**：10_Reference/projects/active/Quartz部署|Quartz 站点]] 自动部署
- 配合 10_Reference/tech-learning/tools/定时任务|cron]]：GitHub Actions 的 `schedule` 触发器是托管态 cron

## 相关链接
- [[10_Reference/tech-learning/MOC]]
- 10_Reference/tech-learning/tools/Git]]
- 10_Reference/tech-learning/tools/定时任务]]
- 10_Reference/projects/active/Quartz部署]]
- 10_Reference/meta/四构件本体方法论]]
