# 🧱 工程地基完成度 Checklist（Phase 2 → Phase 3 门槛）

## 1. CLI 基础执行能力（Execution Layer）

- [ ] 能独立写 argparse CLI
- [ ] 能设计合理命令结构（--word / --top / --char）
- [ ] 能处理文件输入输出
- [ ] 能处理异常（FileNotFound / PermissionError / empty input）

判断标准：
看到需求 → 能直接拆成参数 + 函数结构

达标信号：
- 不需要查语法写 argparse
- 不再边写边想结构

---

## 2. Git 工程流程（Workflow Layer）

- [ ] 熟练 git checkout -b
- [ ] 熟练 git add / commit / push
- [ ] 理解 PR 流程
- [ ] 能看懂 commit history

流程：
Issue → Branch → Commit → Push → PR → Merge

达标信号：
- 不再直接提交 main
- 不再害怕 PR / branch

---

## 3. 测试能力（pytest Layer）

- [ ] 会写 pytest function
- [ ] 会测 normal case
- [ ] 会测 edge case
- [ ] 知道测试是核心流程

结构：
Arrange → Act → Assert

达标信号：
- 写完功能自动补测试

---

## 4. 代码结构能力（Design Layer）

- [ ] 能拆函数
- [ ] 能区分 core logic vs I/O
- [ ] 能做模块拆分
- [ ] 不把所有逻辑写在 main.py

判断标准：
能否3分钟解释项目结构

达标信号：
- 代码可读，而不是仅能运行

---

## 5. 任务拆解能力（Most Important Layer）

- [ ] 一个 feature 能拆 3~5 步
- [ ] 能写 Issue
- [ ] 能控制 feature 粒度

拆解结构：
Feature = 参数设计 + 核心逻辑 + 输出 + 测试 + edge case

达标信号：
- 不再写巨型功能
- 不再边写边改结构

---

## Phase 升级规则

可进入 Phase 3 条件：

- [ ] Git flow 自动化
- [ ] CLI 能独立设计
- [ ] pytest 成为习惯
- [ ] 结构清晰稳定
- [ ] 能稳定拆任务

不满足风险：

AI 用得越多，但无法判断对错，系统能力不会增长

---

## 核心判断

能否在没有 AI 提示的情况下完成一个干净的小功能闭环
