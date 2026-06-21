# Notes Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将独立的 `jay-ai-engineering-notes` 笔记仓库作为 Git submodule 接入 Learning Lab，并提供清晰的分类导航。

**Architecture:** `notes/library/` 保存子模块指针与本地检出内容，`notes/README.md` 作为分类地图，Learning Lab 根 README 只解释这层导航关系。笔记内容和提交历史继续完全属于独立笔记仓库。

**Tech Stack:** Markdown、Git、Git submodule、GitHub

---

### Task 1: 验证目标笔记仓库与本地目录

**Files:**
- Verify: `/Users/jay/Documents/cs-ai-learning/notes/`
- Verify remote: `justlearner010/jay-ai-engineering-notes`

- [ ] **Step 1: 检查目标仓库**

Run:

```bash
gh repo view justlearner010/jay-ai-engineering-notes --json url,isArchived,defaultBranchRef
gh api 'repos/justlearner010/jay-ai-engineering-notes/git/trees/main?recursive=1' --jq '.tree[].path'
```

Expected: 仓库未 Archived，默认分支为 `main`，输出包含 `python/basics`、`python/tooling`、`testing`、`algorithms`、`ai-engineering`、`web/typescript`、`journey/weekly-reviews` 和 `indexes`。

- [ ] **Step 2: 确认旧分类目录为空后删除**

Run:

```bash
find 'notes/algorithm notes' 'notes/python notes' 'notes/typescript notes' -mindepth 1 -print
rmdir 'notes/algorithm notes' 'notes/python notes' 'notes/typescript notes'
```

Expected: `find` 无输出，`rmdir` 成功。任何目录中如果存在文件，必须停止并保留内容。

### Task 2: 添加笔记子模块

**Files:**
- Modify: `/Users/jay/Documents/cs-ai-learning/.gitmodules`
- Create gitlink: `/Users/jay/Documents/cs-ai-learning/notes/library`

- [ ] **Step 1: 添加子模块**

Run:

```bash
git submodule add https://github.com/justlearner010/jay-ai-engineering-notes.git notes/library
```

Expected: `notes/library` 检出笔记仓库 `main`，`.gitmodules` 新增一个条目。

- [ ] **Step 2: 验证子模块身份和分类路径**

Run:

```bash
git -C notes/library remote get-url origin
git -C notes/library status --short --branch
test -d notes/library/python/basics
test -d notes/library/python/tooling
test -d notes/library/testing
test -d notes/library/algorithms
test -d notes/library/ai-engineering
test -d notes/library/web/typescript
test -d notes/library/journey/weekly-reviews
test -f notes/library/indexes/by-topic.md
test -f notes/library/indexes/by-date.md
```

Expected: origin URL 为 `jay-ai-engineering-notes.git`，子模块工作区干净，全部分类与索引存在。

### Task 3: 创建笔记分类地图

**Files:**
- Create: `/Users/jay/Documents/cs-ai-learning/notes/README.md`

- [ ] **Step 1: 创建分类导航页**

Create `notes/README.md` with:

```markdown
# 学习笔记地图

Learning Lab 只负责笔记导航。实际笔记、提交和版本历史继续在 [jay-ai-engineering-notes](https://github.com/justlearner010/jay-ai-engineering-notes) 中独立维护。

## 分类入口

| 分类 | GitHub | 本地路径 |
| --- | --- | --- |
| Python 基础 | [查看](https://github.com/justlearner010/jay-ai-engineering-notes/tree/main/python/basics) | `library/python/basics/` |
| Python 工具链 | [查看](https://github.com/justlearner010/jay-ai-engineering-notes/tree/main/python/tooling) | `library/python/tooling/` |
| 测试 | [查看](https://github.com/justlearner010/jay-ai-engineering-notes/tree/main/testing) | `library/testing/` |
| 算法 | [查看](https://github.com/justlearner010/jay-ai-engineering-notes/tree/main/algorithms) | `library/algorithms/` |
| AI 工程 | [查看](https://github.com/justlearner010/jay-ai-engineering-notes/tree/main/ai-engineering) | `library/ai-engineering/` |
| TypeScript | [查看](https://github.com/justlearner010/jay-ai-engineering-notes/tree/main/web/typescript) | `library/web/typescript/` |
| 历史学习复盘 | [查看](https://github.com/justlearner010/jay-ai-engineering-notes/tree/main/journey/weekly-reviews) | `library/journey/weekly-reviews/` |

## 索引

- [按主题查找](https://github.com/justlearner010/jay-ai-engineering-notes/blob/main/indexes/by-topic.md) — 本地：`library/indexes/by-topic.md`
- [按日期查找](https://github.com/justlearner010/jay-ai-engineering-notes/blob/main/indexes/by-date.md) — 本地：`library/indexes/by-date.md`

## 维护方式

1. 在 `notes/library/` 中编辑笔记。
2. 在子模块仓库中提交并推送笔记。
3. 回到 Learning Lab，提交更新后的子模块指针。

克隆或初始化笔记内容：

```bash
git submodule update --init --recursive
```
```

- [ ] **Step 2: 检查 Markdown 格式**

Run: `git diff --check -- notes/README.md`

Expected: 无输出，退出码为 `0`。

### Task 4: 更新 Learning Lab 根导航

**Files:**
- Modify: `/Users/jay/Documents/cs-ai-learning/README.md`

- [ ] **Step 1: 更新仓库结构表**

Replace the current `notes/` row with:

```markdown
| [`notes/`](./notes/) | 独立笔记仓库的分类地图与子模块入口 |
```

- [ ] **Step 2: 增加笔记导航说明**

Add before `## 关联项目`:

```markdown
## 笔记导航

Learning Lab 只作为笔记地图。实际内容位于独立的 [jay-ai-engineering-notes](https://github.com/justlearner010/jay-ai-engineering-notes) 仓库，可以从 [`notes/`](./notes/) 按主题访问。
```

The existing `git clone --recurse-submodules` and `git submodule update --init --recursive` instructions remain unchanged because they already cover the notes submodule.

### Task 5: 验证、提交并推送

**Files:**
- Commit: `/Users/jay/Documents/cs-ai-learning/.gitmodules`
- Commit: `/Users/jay/Documents/cs-ai-learning/notes/library`
- Commit: `/Users/jay/Documents/cs-ai-learning/notes/README.md`
- Commit: `/Users/jay/Documents/cs-ai-learning/README.md`
- Commit: `/Users/jay/Documents/cs-ai-learning/docs/superpowers/plans/2026-06-21-notes-navigation.md`

- [ ] **Step 1: 验证远程分类链接**

Run:

```bash
for repo_path in python/basics python/tooling testing algorithms ai-engineering web/typescript journey/weekly-reviews indexes/by-topic.md indexes/by-date.md; do
  gh api "repos/justlearner010/jay-ai-engineering-notes/contents/$repo_path?ref=main" >/dev/null
done
```

Expected: 全部 GitHub API 请求成功。

- [ ] **Step 2: 验证本地状态与变更范围**

Run:

```bash
git diff --check
git submodule status
test -z "$(git -C notes/library status --porcelain)"
git status --short --branch
```

Expected: Markdown 无格式错误；`notes/library` 显示提交哈希；子模块干净；`.obsidian/` 仍未跟踪。

- [ ] **Step 3: 明确暂存本次文件**

Run:

```bash
git add .gitmodules README.md notes/README.md notes/library docs/superpowers/plans/2026-06-21-notes-navigation.md
git diff --cached --check
git diff --cached --stat
```

Expected: 暂存区只包含导航文档、计划、`.gitmodules` 和笔记子模块指针。

- [ ] **Step 4: 提交并推送 `main`**

Run:

```bash
git fetch origin main
git merge-base --is-ancestor origin/main HEAD
git commit -m "Add categorized notes navigation"
git push origin main
git fetch origin main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: 本地 `HEAD`、`origin/main` 与远程 `main` 一致。如果远程已新增提交，必须先 rebase 并重新运行验证，不允许强制推送。
