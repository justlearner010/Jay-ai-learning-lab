# Learning Lab README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `README.md` 改写为中文为主的 Learning Lab 仓库入口，并展示学习系统、子模块项目与使用方式。

**Architecture:** README 采用单页导航结构：仓库定位、学习方向、目录地图、关联项目、使用命令、学习循环和英文摘要。子项目继续通过 Git submodule 关联，不复制或修改子仓库源码。

**Tech Stack:** Markdown、Git、Git submodule、GitHub

---

### Task 1: 改写 Learning Lab 入口文档

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 用中文为主的结构替换 README**

README 按照以下顺序编写，不增加还不存在的目录或功能：

1. `# CS & AI Learning Lab`
2. 中文定位：持续学习、项目实践和定期复盘的学习实验室。
3. 当前方向：Python、TypeScript、数据结构、CSAPP、AI Agent。
4. 仓库结构表：`projects/`、`notes/`、`logs/`、`templates/`、`roadmap.md`、`to do list.md`。
5. 关联项目表：AI Reader、TextLab CLI、My Website，同时提供 GitHub 链接和本地子模块路径。
6. 使用方式：完整克隆命令和子模块初始化命令。
7. 学习循环：路线图 → 任务 → 产出 → 复盘。
8. 末尾增加一段简短 `English Summary`。

关键链接和命令必须使用：

```markdown
[roadmap.md](./roadmap.md)
[to do list.md](./to%20do%20list.md)
[AI Reader](https://github.com/justlearner010/ai_reader)
[TextLab CLI](https://github.com/justlearner010/jay-first-cli-text-tool)
[My Website](https://github.com/justlearner010/my_website)
```

```bash
git clone --recurse-submodules https://github.com/justlearner010/Jay-ai-learning-lab.git
git submodule update --init --recursive
```

- [ ] **Step 2: 检查 Markdown 格式**

Run: `git diff --check -- README.md`

Expected: 命令无输出，退出码为 `0`。

### Task 2: 验证子模块与文档入口

**Files:**
- Verify: `.gitmodules`
- Verify: `README.md`
- Verify: `roadmap.md`
- Verify: `to do list.md`

- [ ] **Step 1: 验证三个子模块**

Run: `git submodule status`

Expected: 输出 `projects/ai-reader`、`projects/jay-first-cli-text-tool` 和 `projects/my_website`，且每项都有提交哈希。

- [ ] **Step 2: 验证本地文档**

Run: `test -f README.md && test -f roadmap.md && test -f 'to do list.md'`

Expected: 命令无输出，退出码为 `0`。

### Task 3: 提交并推送相关改动

**Files:**
- Commit: `.gitmodules`
- Commit: `README.md`
- Commit: `roadmap.md`
- Commit: `projects/ai-reader`
- Commit: `projects/jay-first-cli-text-tool`
- Commit: `projects/my_website`
- Commit: `docs/superpowers/plans/2026-06-21-learning-lab-readme.md`

- [ ] **Step 1: 明确暂存文件**

Run:

```bash
git add .gitmodules README.md roadmap.md projects/ai-reader projects/jay-first-cli-text-tool projects/my_website docs/superpowers/plans/2026-06-21-learning-lab-readme.md
```

Expected: 不暂存 `.obsidian/`，因为它包含本机工作区状态。

- [ ] **Step 2: 创建提交**

Run: `git commit -m "Build learning lab project hub"`

Expected: 提交包含 README、roadmap、`.gitmodules`、三个子模块入口和实施计划。

- [ ] **Step 3: 推送主分支**

Run: `git push origin main`

Expected: 远程 `main` 更新到本地最新提交。

- [ ] **Step 4: 验证远程同步**

Run:

```bash
git fetch origin main
git rev-parse HEAD
git rev-parse origin/main
git status --short --branch
```

Expected: `HEAD` 与 `origin/main` 哈希相同；只余本机 `.obsidian/` 未跟踪内容。
