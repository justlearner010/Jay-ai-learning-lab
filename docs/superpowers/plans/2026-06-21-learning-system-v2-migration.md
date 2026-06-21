# Learning System v2 Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `Jay-ai-learning-lab` 升级为轻量、自由的唯一学习入口，并将旧 `jay-ai-agent-learning-system` 安全快照到归档仓库后设为只读。

**Architecture:** 迁移分为三个有顺序的仓库操作：先复制并验证旧系统快照，再更新旧仓库的迁移入口，然后升级 Learning Lab，最后才设置 GitHub Archived 状态。任何快照、安全或远程同步验证失败都必须阻止最后归档动作。

**Tech Stack:** Markdown、Git、GitHub CLI、Git archive

---

### Task 1: 准备三仓库工作区

**Files:**
- Verify: `/Users/jay/Documents/cs-ai-learning`
- Create checkout: `/Users/jay/Documents/codex-learning-system-migration/legacy`
- Create checkout: `/Users/jay/Documents/codex-learning-system-migration/archive`

- [ ] **Step 1: 检查 GitHub 登录与仓库状态**

Run:

```bash
gh auth status
gh repo view justlearner010/Jay-ai-learning-lab --json url,isArchived,defaultBranchRef
gh repo view justlearner010/jay-ai-agent-learning-system --json url,isArchived,defaultBranchRef
gh repo view justlearner010/jay-ai-agent-roadmap-archive --json url,isArchived,defaultBranchRef
```

Expected: 三个仓库均可访问；旧学习系统尚未 Archived；默认分支均为 `main`。

- [ ] **Step 2: 创建临时迁移目录并克隆两个远程仓库**

Run:

```bash
mkdir -p /Users/jay/Documents/codex-learning-system-migration
gh repo clone justlearner010/jay-ai-agent-learning-system /Users/jay/Documents/codex-learning-system-migration/legacy
gh repo clone justlearner010/jay-ai-agent-roadmap-archive /Users/jay/Documents/codex-learning-system-migration/archive
```

Expected: 两个克隆命令成功，两个工作区都位于 `main`。如果目录已存在，先用 `git -C <path> status --short --branch` 验证它是目标仓库且工作区干净，不要覆盖。

### Task 2: 锁定源快照并执行安全检查

**Files:**
- Verify repository: `/Users/jay/Documents/codex-learning-system-migration/legacy`
- Create: `/Users/jay/Documents/codex-learning-system-migration/legacy-files.txt`

- [ ] **Step 1: 验证源提交并生成文件清单**

Run:

```bash
git -C /Users/jay/Documents/codex-learning-system-migration/legacy pull --ff-only origin main
git -C /Users/jay/Documents/codex-learning-system-migration/legacy rev-parse HEAD
git -C /Users/jay/Documents/codex-learning-system-migration/legacy ls-files | sort > /Users/jay/Documents/codex-learning-system-migration/legacy-files.txt
```

Expected: 源提交为 `be56030ad81ddac88f0f173b5e579dde51cf2411`，工作区干净。如果提交已变更，将实际哈希用于归档元数据，并在提交前重新检查差异。

- [ ] **Step 2: 扫描敏感路径和敏感内容**

Run:

```bash
git -C /Users/jay/Documents/codex-learning-system-migration/legacy ls-files | rg '(^|/)(\.env($|\.)|.*\.(pem|key|p12|pfx)$|id_rsa$)'
git -C /Users/jay/Documents/codex-learning-system-migration/legacy grep -IlE '(BEGIN (RSA |OPENSSH )?PRIVATE KEY|gh[opsu]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,})' -- .
```

Expected: 两条命令都无输出。任何命中都必须停止迁移并先审核文件，不得直接推送。

### Task 3: 创建并推送旧系统快照

**Files:**
- Create: `/Users/jay/Documents/codex-learning-system-migration/archive/learning-system-archive/**`
- Create: `/Users/jay/Documents/codex-learning-system-migration/archive/learning-system-archive/ARCHIVE-METADATA.md`
- Modify: `/Users/jay/Documents/codex-learning-system-migration/archive/README.md`

- [ ] **Step 1: 从已锁定提交导出受跟踪文件**

Run:

```bash
test ! -e /Users/jay/Documents/codex-learning-system-migration/archive/learning-system-archive
mkdir -p /Users/jay/Documents/codex-learning-system-migration/archive/learning-system-archive
git -C /Users/jay/Documents/codex-learning-system-migration/legacy archive --format=tar HEAD | tar -xf - -C /Users/jay/Documents/codex-learning-system-migration/archive/learning-system-archive
```

Expected: `learning-system-archive/` 仅包含源提交中受 Git 跟踪的文件，不包含 `.git/`。

- [ ] **Step 2: 新增归档元数据**

Create `learning-system-archive/ARCHIVE-METADATA.md` with:

```markdown
# Learning System Archive Metadata

- 来源仓库：https://github.com/justlearner010/jay-ai-agent-learning-system
- 归档日期：2026-06-21
- 源分支：`main`
- 源提交：`be56030ad81ddac88f0f173b5e579dde51cf2411`
- 归档原因：旧系统的固定 AI Agent 学习节奏已被更自由的 Learning Lab 取代。
- 新入口：https://github.com/justlearner010/Jay-ai-learning-lab

> 本目录是历史快照，不再维护。原仓库保留完整 Git 历史。
```

If Task 2 found a newer source commit, replace only the source commit value with that verified hash.

- [ ] **Step 3: 在归档仓库 README 顶部增加快照入口**

Add below the opening archive notice:

```markdown
## 归档入口

- [旧 AI Agent 学习路线](./roadmap.md)
- [旧 AI Agent 学习系统快照](./learning-system-archive/)
- [当前 Learning Lab](https://github.com/justlearner010/Jay-ai-learning-lab)
```

- [ ] **Step 4: 验证快照文件清单**

Run:

```bash
cd /Users/jay/Documents/codex-learning-system-migration/archive
find learning-system-archive -type f ! -name ARCHIVE-METADATA.md -print | sed 's#^learning-system-archive/##' | sort > ../archived-files.txt
diff -u ../legacy-files.txt ../archived-files.txt
git diff --check
```

Expected: `diff` 无输出，`git diff --check` 无格式错误。

- [ ] **Step 5: 提交、推送并验证归档仓库**

Run:

```bash
git add README.md learning-system-archive
git commit -m "Archive legacy AI Agent learning system"
git push origin main
git fetch origin main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: 归档快照已上传，本地 `HEAD` 与 `origin/main` 一致。

### Task 4: 更新旧学习系统迁移说明

**Files:**
- Modify: `/Users/jay/Documents/codex-learning-system-migration/legacy/README.md`

- [ ] **Step 1: 将 README 顶部替换为归档通知**

README 顶部必须包含：

```markdown
# AI Agent Learning System（已归档）

> 本仓库已于 2026-06-21 停止维护。原有路线、任务库、模板和自动化保留用于历史查阅。

## 当前入口

- [CS & AI Learning Lab](https://github.com/justlearner010/Jay-ai-learning-lab)
- [归档快照](https://github.com/justlearner010/jay-ai-agent-roadmap-archive/tree/main/learning-system-archive)

---
```

Keep the remaining historical README below the divider so existing context is not deleted.

- [ ] **Step 2: 验证、提交并推送旧仓库**

Run:

```bash
cd /Users/jay/Documents/codex-learning-system-migration/legacy
git diff --check
git add README.md
git commit -m "Point archived learning system to Learning Lab"
git push origin main
git fetch origin main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: 迁移通知已上传，原有内容仍保留。

### Task 5: 升级 Learning Lab 的日志与总结系统

**Files:**
- Create: `/Users/jay/Documents/cs-ai-learning/logs/README.md`
- Create: `/Users/jay/Documents/cs-ai-learning/summary/README.md`
- Create: `/Users/jay/Documents/cs-ai-learning/summary/weekly/.gitkeep`
- Create: `/Users/jay/Documents/cs-ai-learning/summary/monthly/.gitkeep`
- Create: `/Users/jay/Documents/cs-ai-learning/summary/phases/.gitkeep`
- Create: `/Users/jay/Documents/cs-ai-learning/templates/daily-log.md`
- Create: `/Users/jay/Documents/cs-ai-learning/templates/weekly-summary.md`
- Create: `/Users/jay/Documents/cs-ai-learning/templates/phase-summary.md`
- Modify: `/Users/jay/Documents/cs-ai-learning/README.md`

- [ ] **Step 1: 创建轻量日志模板**

Create `templates/daily-log.md`:

```markdown
# YYYY-MM-DD

- 今天推进了什么：
- 证据或结果：
- 下一步最自然的动作：
```

- [ ] **Step 2: 创建周总结和阶段总结模板**

Create `templates/weekly-summary.md`:

```markdown
# YYYY-Www 周总结

## 本周真正推进了什么？

## 有哪些可验证成果？

## 哪个知识点变清楚了？

## 哪些计划被删除或调整了？

## 下周只保留哪个重点？
```

Create `templates/phase-summary.md`:

```markdown
# Phase X 总结

## 阶段目标

## 主要成果

## 能力变化

## 放弃或调整的事项

## 下一阶段方向
```

- [ ] **Step 3: 创建日志与总结使用说明**

`logs/README.md` 必须说明：日志可选、只记录当下、使用 `YYYY-MM-DD.md` 命名、不统计时长、不需补记。

`summary/README.md` 必须说明：周总结位于 `weekly/`，月总结位于 `monthly/`，阶段总结位于 `phases/`，只把经复盘确认的方向变更写回 `roadmap.md`。

Create the summary directories and their tracked placeholders:

```bash
mkdir -p summary/weekly summary/monthly summary/phases
touch summary/weekly/.gitkeep summary/monthly/.gitkeep summary/phases/.gitkeep
```

- [ ] **Step 4: 更新 Learning Lab README 目录表和学习循环**

README 的仓库结构表必须增加 `summary/`，并将 `logs/` 描述为可选轻量日志。学习循环改为：

```text
路线图 → 当前行动 → 可选日志 → 周/阶段总结 → 更新路线图
```

- [ ] **Step 5: 验证、提交并推送 Learning Lab**

Run:

```bash
cd /Users/jay/Documents/cs-ai-learning
git diff --check
test -f templates/daily-log.md
test -f templates/weekly-summary.md
test -f templates/phase-summary.md
test -f summary/README.md
git add README.md logs/README.md summary templates/daily-log.md templates/weekly-summary.md templates/phase-summary.md docs/superpowers/plans/2026-06-21-learning-system-v2-migration.md
git commit -m "Introduce flexible learning system v2"
git push origin main
git fetch origin main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: Learning Lab 的新结构、模板、设计与实施计划已上传；`.obsidian/` 仍未跟踪。

### Task 6: 设置旧仓库为 Archived 并执行最终验证

**External state:**
- Update: `justlearner010/jay-ai-agent-learning-system` GitHub repository metadata

- [ ] **Step 1: 在归档前重新验证三个远程仓库**

Run:

```bash
test "$(git -C /Users/jay/Documents/codex-learning-system-migration/archive rev-parse HEAD)" = "$(git -C /Users/jay/Documents/codex-learning-system-migration/archive rev-parse origin/main)"
test "$(git -C /Users/jay/Documents/codex-learning-system-migration/legacy rev-parse HEAD)" = "$(git -C /Users/jay/Documents/codex-learning-system-migration/legacy rev-parse origin/main)"
test "$(git -C /Users/jay/Documents/cs-ai-learning rev-parse HEAD)" = "$(git -C /Users/jay/Documents/cs-ai-learning rev-parse origin/main)"
gh api 'repos/justlearner010/jay-ai-agent-roadmap-archive/contents/learning-system-archive/ARCHIVE-METADATA.md?ref=main' --jq .sha
```

Expected: 三个远程均已同步，归档元数据可从 GitHub 读取。

- [ ] **Step 2: 将旧学习系统设为 Archived**

Run:

```bash
gh api --method PATCH repos/justlearner010/jay-ai-agent-learning-system -f archived=true --jq '{full_name, archived}'
```

Expected: 输出 `archived: true`。

- [ ] **Step 3: 验证最终状态**

Run:

```bash
gh repo view justlearner010/jay-ai-agent-learning-system --json url,isArchived
gh repo view justlearner010/jay-ai-agent-roadmap-archive --json url,isArchived
gh repo view justlearner010/Jay-ai-learning-lab --json url,isArchived
git -C /Users/jay/Documents/cs-ai-learning status --short --branch
```

Expected: 旧学习系统 `isArchived: true`；归档仓库与 Learning Lab 仍为活跃状态；Learning Lab 只剩 `.obsidian/` 未跟踪内容。
