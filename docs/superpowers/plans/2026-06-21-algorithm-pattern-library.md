# Phase 2 Algorithm Pattern Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing algorithm notes into a pattern-first interview practice system and add a curated 12-problem Phase 2 route derived from Algo-Atlas.

**Architecture:** Keep all algorithm learning content in the existing `notes/library` Git submodule. Separate navigation, curated backlog, reusable pattern summaries, per-problem evidence, and review history; commit content inside the notes repository first, then update the parent Learning Lab submodule pointer.

**Tech Stack:** Markdown, Python 3 interview solutions, Git, Git submodules, GitHub links

---

## File map

Files created inside `notes/library`:

- `algorithms/README.md`: algorithm area entry point and Phase 2 dashboard.
- `algorithms/problem-set.md`: sourced, ordered 12-problem backlog.
- `algorithms/patterns/hash-map.md`: first reusable pattern summary based on six existing notes.
- `algorithms/templates/problem-note.md`: compact per-problem evidence template.
- `algorithms/review-log.md`: append-only review outcomes.
- `algorithms/problems/hash-map/README.md`: links the six migrated baseline problems.
- `algorithms/problems/two-pointers/README.md`: points to the six selected Two Pointers backlog items.
- `algorithms/problems/sliding-window/README.md`: points to the six selected Sliding Window backlog items.

Directories created inside `notes/library`:

- `algorithms/problems/hash-map/`
- `algorithms/problems/two-pointers/`
- `algorithms/problems/sliding-window/`
- `algorithms/patterns/`
- `algorithms/templates/`

Existing files moved inside `notes/library`:

- `algorithms/001-two-sum.md` → `algorithms/problems/hash-map/001-two-sum.md`
- `algorithms/002-contains-duplicate.md` → `algorithms/problems/hash-map/002-contains-duplicate.md`
- `algorithms/003-valid-anagram.md` → `algorithms/problems/hash-map/003-valid-anagram.md`
- `algorithms/004-ransom-note.md` → `algorithms/problems/hash-map/004-ransom-note.md`
- `algorithms/005-group-anagrams.md` → `algorithms/problems/hash-map/005-group-anagrams.md`
- `algorithms/006-top-k-frequent-elements.md` → `algorithms/problems/hash-map/006-top-k-frequent-elements.md`

Files modified inside `notes/library`:

- `indexes/by-topic.md`: replace old direct paths with the new algorithm entry point and problem paths.
- `indexes/by-date.md`: replace moved algorithm paths.

Files modified in the parent Learning Lab:

- `roadmap.md`: link the Phase 2 algorithm task to the algorithm dashboard and state the selected route.
- `to do list.md`: replace the vague daily-practice item with the four-week measurable cadence.
- `notes/library`: record the new notes submodule commit.

### Task 1: Create the sourced Phase 2 problem route

**Files:**
- Create: `notes/library/algorithms/problem-set.md`

- [ ] **Step 1: Write the source and selection policy**

Start the file with this content:

```markdown
# Phase 2 面试算法题集

本题集借鉴 [lvy010/Algo-Atlas](https://github.com/lvy010/Algo-Atlas) 的早期学习顺序，并根据当前 Python 基础、一个月周期和面试模式识别目标进行缩减。

路线：Hash Map 基线复刷 → Two Pointers → Sliding Window。

筛选原则：

- 优先保留能形成可复用模式的代表题。
- Phase 2 只增加 12 道新题，不追求原仓库规模。
- 现有 6 道 Hash Map 题用于复刷和模式总结，不计入 12 道新题。
- 未完成的题只存在于题集，不提前创建空白题解。
```

- [ ] **Step 2: Add the exact four-week backlog**

Add this table with each LeetCode title linked to its official problem page:

```markdown
| 周次 | 顺序 | 模式 | 题目 | 难度 | 状态 |
| --- | ---: | --- | --- | --- | --- |
| Week 1 | 1 | Two Pointers | [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/) | Easy | `backlog` |
| Week 1 | 2 | Two Pointers | [202. Happy Number](https://leetcode.com/problems/happy-number/) | Easy | `backlog` |
| Week 1 | 3 | Two Pointers | [167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium | `backlog` |
| Week 2 | 4 | Two Pointers | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | `backlog` |
| Week 2 | 5 | Two Pointers | [15. 3Sum](https://leetcode.com/problems/3sum/) | Medium | `backlog` |
| Week 2 | 6 | Two Pointers | [18. 4Sum](https://leetcode.com/problems/4sum/) | Medium | `backlog` |
| Week 3 | 7 | Sliding Window | [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Medium | `backlog` |
| Week 3 | 8 | Sliding Window | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | `backlog` |
| Week 3 | 9 | Sliding Window | [1004. Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | Medium | `backlog` |
| Week 4 | 10 | Sliding Window | [904. Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | Medium | `backlog` |
| Week 4 | 11 | Sliding Window | [1658. Minimum Operations to Reduce X to Zero](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/) | Medium | `backlog` |
| Week 4 | 12 | Sliding Window | [438. Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | Medium | `backlog` |
```

- [ ] **Step 3: Add status semantics**

Define the allowed backlog states exactly as:

```markdown
## 状态

- `backlog`：尚未开始。
- `learning`：已经尝试，但不能稳定独立完成。
- `review`：已经理解，等待无提示复刷。
- `mastered`：无提示独立完成，并能解释模式、复杂度和边界条件。
```

- [ ] **Step 4: Validate the problem-set file**

Run:

```bash
rg -n "Algo-Atlas|Week [1-4]|backlog|mastered" algorithms/problem-set.md
```

Expected: one source reference, 12 problem rows distributed across four weeks, and all four statuses documented.

- [ ] **Step 5: Commit the curated route in the notes repository**

```bash
git -C notes/library add algorithms/problem-set.md
git -C notes/library commit -m "Add Phase 2 algorithm problem route"
```

### Task 2: Add the pattern-library navigation and evidence templates

**Files:**
- Create: `notes/library/algorithms/README.md`
- Create: `notes/library/algorithms/templates/problem-note.md`
- Create: `notes/library/algorithms/review-log.md`
- Create: `notes/library/algorithms/problems/hash-map/README.md`
- Create: `notes/library/algorithms/problems/two-pointers/README.md`
- Create: `notes/library/algorithms/problems/sliding-window/README.md`

- [ ] **Step 1: Create the algorithm dashboard**

Write `algorithms/README.md` with these sections and links:

```markdown
# 面试算法模式库

目标：通过模式识别、独立实现和定期复刷准备技术面试，而不是累计题量。

## Phase 2

- [精选题集](./problem-set.md)
- [复刷记录](./review-log.md)
- [单题模板](./templates/problem-note.md)

## 模式

| 模式 | 状态 | 总结 | 题目目录 |
| --- | --- | --- | --- |
| Hash Map / Set | 基线整理 | [模式总结](./patterns/hash-map.md) | [题目](./problems/hash-map/) |
| Two Pointers | Phase 2 | 完成 3 题后创建 | [题目](./problems/two-pointers/) |
| Sliding Window | Phase 2 | 完成 3 题后创建 | [题目](./problems/sliding-window/) |

## 每周节奏

- 3 道新题。
- 2 道无提示复刷。
- 周末更新题集状态和复刷记录。

## 完成定义

一道题只有在无提示独立完成，并能解释模式、复杂度和至少两个边界条件后，才能标记为 `mastered`。
```

- [ ] **Step 2: Create the compact problem-note template**

Write `algorithms/templates/problem-note.md` using these defined template variables: `{{id}}`, `{{title}}`, `{{url}}`, `{{difficulty}}`, `{{pattern}}`, `{{date}}`.

Required headings:

```markdown
# {{id}}. {{title}}

## 题目信息
## 题意复述
## 模式识别信号
## 第一次思路与卡点
## 最终解法
## Python 实现
## 复杂度
## 边界条件
## 错误记录
## 面试表达
## 复刷记录
```

Under `复刷记录`, include the same columns as `review-log.md` so evidence can be copied without reinterpretation.

- [ ] **Step 3: Create the centralized review log**

Write `algorithms/review-log.md`:

```markdown
# 算法复刷记录

复刷前不阅读旧答案。先独立写代码并口头解释，再记录结果。

| 日期 | 题目 | 模式 | 用时 | 是否独立完成 | 状态 | 下次复刷 | 主要问题 |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

- [ ] **Step 4: Create only the three in-scope directories**

```bash
mkdir -p notes/library/algorithms/problems/{hash-map,two-pointers,sliding-window}
mkdir -p notes/library/algorithms/{patterns,templates}
```

Do not create directories for dynamic programming, graphs, trees, or other future topics.

- [ ] **Step 5: Add a focused README to each problem directory**

Each directory README must state its pattern, link back to `../../README.md` and `../../problem-set.md`, and list only the problems assigned to that pattern. The Hash Map README links the six migrated files; the other two READMEs link the six official LeetCode backlog URLs for their pattern and explicitly say that local solution files are created only after a real attempt.

- [ ] **Step 6: Validate navigation targets**

Run:

```bash
test -f notes/library/algorithms/README.md
test -f notes/library/algorithms/problem-set.md
test -f notes/library/algorithms/templates/problem-note.md
test -f notes/library/algorithms/review-log.md
test -f notes/library/algorithms/problems/hash-map/README.md
test -f notes/library/algorithms/problems/two-pointers/README.md
test -f notes/library/algorithms/problems/sliding-window/README.md
```

Expected: all commands exit with status 0.

- [ ] **Step 7: Commit the dashboard and templates in the notes repository**

```bash
git -C notes/library add algorithms/README.md algorithms/templates/problem-note.md algorithms/review-log.md algorithms/problems/*/README.md
git -C notes/library commit -m "Add algorithm pattern library workflow"
```

### Task 3: Migrate the six existing Hash Map notes without inventing evidence

**Files:**
- Move: the six files listed in the file map to `notes/library/algorithms/problems/hash-map/`
- Modify: `notes/library/indexes/by-topic.md`
- Modify: `notes/library/indexes/by-date.md`

- [ ] **Step 1: Move files with Git history preserved**

Run six `git mv` commands from inside `notes/library`, for example:

```bash
git mv algorithms/001-two-sum.md algorithms/problems/hash-map/001-two-sum.md
git mv algorithms/002-contains-duplicate.md algorithms/problems/hash-map/002-contains-duplicate.md
git mv algorithms/003-valid-anagram.md algorithms/problems/hash-map/003-valid-anagram.md
git mv algorithms/004-ransom-note.md algorithms/problems/hash-map/004-ransom-note.md
git mv algorithms/005-group-anagrams.md algorithms/problems/hash-map/005-group-anagrams.md
git mv algorithms/006-top-k-frequent-elements.md algorithms/problems/hash-map/006-top-k-frequent-elements.md
```

- [ ] **Step 2: Update the topic index**

Add `algorithms/README.md` as the primary algorithm link and replace every old `algorithms/00X-...md` path with `algorithms/problems/hash-map/00X-...md`.

- [ ] **Step 3: Update the date index**

Replace every old algorithm path with its new `algorithms/problems/hash-map/` path. Do not assign fabricated source dates to files whose original date is unknown.

- [ ] **Step 4: Verify there are no stale moved paths**

Run:

```bash
rg -n "algorithms/00[1-6]-" notes/library --glob '*.md'
```

Expected: no matches.

- [ ] **Step 5: Commit the migration in the notes repository**

```bash
git -C notes/library add algorithms indexes/by-topic.md indexes/by-date.md
git -C notes/library commit -m "Organize existing problems by algorithm pattern"
```

### Task 4: Consolidate the first reusable Hash Map pattern

**Files:**
- Create: `notes/library/algorithms/patterns/hash-map.md`
- Modify: six files under `notes/library/algorithms/problems/hash-map/`

- [ ] **Step 1: Create the Hash Map pattern summary**

Write sections for recognition signals, set versus dictionary selection, frequency counting, complement lookup, grouping-key design, Top K follow-up, complexity, common mistakes, and representative links to all six migrated problems.

Include these minimum reusable Python shapes:

```python
# Membership / duplicate detection
seen = set()
for item in items:
    if item in seen:
        return True
    seen.add(item)
```

```python
# Complement lookup
seen = {}
for index, value in enumerate(values):
    needed = target - value
    if needed in seen:
        return [seen[needed], index]
    seen[value] = index
```

```python
# Frequency counting
from collections import Counter

counts = Counter(items)
```

- [ ] **Step 2: Normalize status fields conservatively**

For each existing note, replace the multiple-choice status placeholder with exactly one of `learning` or `review`, based only on evidence already written in that note. Do not mark any existing problem `mastered` without a new no-hint review result.

- [ ] **Step 3: Remove empty boilerplate without filling user knowledge**

Delete empty bullet placeholders and unused sections. Preserve all existing user-authored reasoning, code, mistakes, dates, and explanations. If an unresolved issue matters, express it as a concrete `需要复刷确认` line.

- [ ] **Step 4: Add cross-links**

Each problem note must link back to `../../patterns/hash-map.md` and `../../README.md`. The pattern summary must link to all six problem notes using relative paths.

- [ ] **Step 5: Check for invalid completion claims and placeholders**

Run:

```bash
rg -n "mastered|YYYY-MM-DD|状态：.* / |^- *$" notes/library/algorithms/problems/hash-map notes/library/algorithms/patterns/hash-map.md
```

Expected: no unjustified `mastered` status, no template dates, no multiple-choice status fields, and no empty bullet placeholders.

- [ ] **Step 6: Commit the first pattern in the notes repository**

```bash
git -C notes/library add algorithms/patterns/hash-map.md algorithms/problems/hash-map
git -C notes/library commit -m "Build reusable Hash Map interview pattern"
```

### Task 5: Validate and publish the notes submodule changes

**Files:**
- Verify: all files under `notes/library/algorithms/`

- [ ] **Step 1: Check whitespace and repository status**

```bash
git -C notes/library diff --check HEAD~4..HEAD
git -C notes/library status --short --branch
```

Expected: no whitespace errors and a clean working tree after the four planned notes commits.

- [ ] **Step 2: Verify all required links resolve locally**

Check each relative Markdown link under `algorithms/README.md`, `algorithms/patterns/hash-map.md`, `indexes/by-topic.md`, and `indexes/by-date.md` against the filesystem.

Expected: zero missing local targets. External LeetCode and Algo-Atlas URLs remain explicit source links.

- [ ] **Step 3: Push the notes repository normally**

```bash
git -C notes/library push origin main
```

Expected: push succeeds without force and GitHub `main` contains the four new commits.

### Task 6: Connect the pattern library to the parent Learning Lab

**Files:**
- Modify: `roadmap.md`
- Modify: `to do list.md`
- Modify: `notes/library` submodule pointer

- [ ] **Step 1: Update the Phase 2 roadmap task**

Replace the vague Algo-Atlas task with a link to `notes/library/algorithms/README.md` and state this exact scope: Hash Map baseline review, 6 Two Pointers problems, 6 Sliding Window problems, 3 new problems plus 2 reviews per week.

- [ ] **Step 2: Update the current task list**

Replace “每日的算法练习” with four weekly checklist items matching `algorithms/problem-set.md`. Do not require a seven-day streak.

- [ ] **Step 3: Verify the parent repository only records intended changes**

```bash
git status --short
git diff -- roadmap.md "to do list.md"
git diff --submodule=short -- notes/library
```

Expected: pre-existing user changes remain intact; the algorithm integration is visible and the submodule pointer references the pushed notes commit.

- [ ] **Step 4: Commit only the Phase 2 integration files**

```bash
git add roadmap.md "to do list.md" notes/library
git commit -m "Integrate Phase 2 algorithm pattern route"
```

- [ ] **Step 5: Run final verification**

```bash
git diff --check HEAD^..HEAD
git submodule status notes/library
git status --short --branch
```

Expected: the parent commit has no whitespace errors, `notes/library` points to the pushed notes commit, and unrelated local files remain unstaged.
