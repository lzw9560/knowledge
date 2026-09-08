---
type: project
name: quartz-site
title: Quartz 静态站点
status: 待启动
created: 2026-09-07
---

# quartz-site

## 项目概述
基于 [Quartz](https://quartz.jzhao.xyz/) 的 Obsidian Vault 静态站点发布工具。把本知识图谱 vault 发布为可导航的公开网站。

## 状态
- **刚部署**：站点已上线，但内容/主题/导航待完善
- 待办：MOC 页面样式调优、搜索配置、SEO、自定义域名

## 技术栈
- 站点生成器：Quartz（基于 [[10_Reference/tech-learning/frameworks/vite|Vite]] + React）
- 内容源：本 Obsidian Vault（10_Reference/projects/active/知识图谱|knowledge-graph 元项目]]）
- 部署：静态托管（GitHub Pages / Cloudflare Pages）

## 与知识图谱的关系
- quartz-site 是 knowledge-graph vault 的**发布层**
- vault 本地用 10_Reference/tech-learning/tools/Obsidian|Obsidian]] 编辑，Quartz 负责生成公开站点
- 内容同源：不维护两份，Quartz 直接读 vault 的 `.md` 文件

## 相关链接
- [[10_Reference/projects/MOC]]
- 10_Reference/projects/active/知识图谱]]
- [[10_Reference/tech-learning/MOC]]
- 10_Reference/tech-learning/tools/Obsidian]]
- 10_Reference/meta/四构件本体方法论]]
