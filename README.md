# CS & AI Learning Lab

> 一个用于持续学习、项目实践和定期复盘的 CS / AI Agent 学习实验室。

## 关于这个 Learning Lab

这个仓库是我的 CS 与 AI Agent 学习系统总入口。它不只保存零散笔记，而是将学习过程组织为可追踪、可复盘、可展示的长期资产。

每个学习阶段尽量产出项目、笔记、测试、文档和复盘记录，而不只是完成一次性任务。

## 当前学习方向

- Python 工程化
- TypeScript 基础
- 数据结构与算法
- CSAPP 与计算机系统基础
- AI Agent 应用与工程实践

## 仓库结构

| 路径                                     | 用途                      |
| -------------------------------------- | ----------------------- |
| [`projects/`](./projects)              | 以 Git submodule 关联的实践项目 |
| [`notes/`](./notes/)                   | 独立笔记仓库的分类地图与子模块入口       |
| [`logs/`](./logs/)                     | 可选的轻量学习日志               |
| [`summary/`](./summary/)               | 周、月度和阶段总结               |
| [`templates/`](./templates/)           | 轻量日志、总结和开发任务说明模板        |
| [`AGENTS.md`](./AGENTS.md)             | AI / 自动化协作时的仓库操作协议       |
| [`docs/`](./docs/)                     | 工作流说明、设计记录和 AI 操作上下文     |
| [`roadmap.md`](./roadmap.md)           | 阶段性学习路线与优先级             |
| [`archives/`](./archives/)             | 历史学习文件、计划归档             |
| [`to do list.md`](./to%20do%20list.md) | 当前任务清单                  |
| [`incubator/`](./incubator)            | 项目孵化池，用于将脑中的想法孵化成实际项目   |

## 笔记导航

Learning Lab 只作为笔记地图。实际内容位于独立的 [jay-ai-engineering-notes](https://github.com/justlearner010/jay-ai-engineering-notes) 仓库，可以从 [`notes/`](./notes/) 按主题访问。

## 关联项目

| 项目 | 定位 | 本地路径 |
| --- | --- | --- |
| [AI Reader](https://github.com/justlearner010/ai_reader) | 支持 AI 解释、翻译和笔记的阅读器 | [`projects/ai-reader`](./projects/ai-reader) |
| [TextLab CLI](https://github.com/justlearner010/jay-first-cli-text-tool) | 用于文本统计、分块和测试练习的 Python CLI | [`projects/jay-first-cli-text-tool`](./projects/jay-first-cli-text-tool) |
| [My Website](https://github.com/justlearner010/my_website) | 个人网站与项目展示入口 | [`projects/my_website`](./projects/my_website) |

## 如何使用

完整克隆仓库及其关联项目：

```bash
git clone --recurse-submodules https://github.com/justlearner010/Jay-ai-learning-lab.git
```

如果已经普通克隆了仓库，可以再初始化子模块：

```bash
git submodule update --init --recursive
```

## 学习循环

1. 在 [`roadmap.md`](./roadmap.md) 中确定阶段方向。
2. 在 [`to do list.md`](./to%20do%20list.md) 中选择当前行动。
3. 按需在 [`logs/`](./logs/) 中留下简单的进展和证据。
4. 在 [`summary/`](./summary/) 中完成周总结或阶段总结。
5. 只把经过复盘确认的方向变化更新回路线图。

> 路线图 → 当前行动 → 可选日志 → 周/阶段总结 → 更新路线图

## AI / Obsidian 协作入口

AI 会话先读取 [`AGENTS.md`](./AGENTS.md) 和 [`docs/ai-operating-manual.md`](./docs/ai-operating-manual.md)。这两份文件定义了目录边界、复习卡规则、任务分流方式，以及哪些内容不能由 AI 擅自推断。

## English Summary

This repository is my structured CS and AI Agent learning lab. It connects hands-on projects, technical notes, roadmaps, task tracking, and regular reviews so that each learning cycle produces visible and reusable outcomes.
