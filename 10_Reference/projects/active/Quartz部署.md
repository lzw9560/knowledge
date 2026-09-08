---
type: project
name: quartz-deploy
title: Quartz 站点部署
status: 活跃
created: 2026-09-07
---

# quartz-deploy

## 项目概述
把本 Obsidian vault 通过 [Quartz](https://quartz.jzhao.xyz/) 发布为静态站点，实现知识图谱的公开镜像。本地编辑 → obsidian-git 同步 → quartz-deploy workflow 构建 → 公网可访问。

## 技术栈
- Quartz v4（Hugo-based 静态站点生成器）
- GitHub Pages / Cloudflare Pages（托管）
- [[10_Reference/tech-learning/tools/GitHub-Actions|GitHub]]（自动部署 workflow）

## 工作流
```
Obsidian 编辑 → obsidian-git push →
  quartz-deploy workflow 触发 →
    Quartz 构建 → 部署到 Pages
```

## 与本知识图谱的链接
- 公开镜像：本 vault 的公开版（敏感项目实体如 [[10_Reference/projects/active/Vibe-Research|Vibe-]] 私有信息过滤后发布）
- [[10_Reference/tech-learning/tools/Obsidian-Git插件|obsidian-]] 是同步层，quartz-deploy 是发布层
- [[10_Reference/projects/backlog/Quartz站点|quartz-]]（候选）→ 本项目即其落地实现，状态升级为活跃

## 相关链接
- [[10_Reference/reading/MOC]]
- [[10_Reference/tech-learning/tools/GitHub-Actions]]
- [[10_Reference/tech-learning/tools/Obsidian-Git插件]]
- [[10_Reference/tech-learning/tools/Git]]
- [[10_Reference/meta/四构件本体方法论]]
