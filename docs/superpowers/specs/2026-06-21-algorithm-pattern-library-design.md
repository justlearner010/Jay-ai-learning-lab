# Phase 2 算法模式库设计

## 1. 目标

在现有 `jay-ai-engineering-notes/algorithms` 中建立面向技术面试的算法模式库。重点不是累计题量，而是训练以下闭环：

> 识别题目特征 → 选择算法模式 → 独立实现 → 解释复杂度 → 定期复刷

本阶段借鉴 [Algo-Atlas](https://github.com/lvy010/Algo-Atlas) 的分类框架、模板提炼和定期复习思路，但不复制其题量、高阶 C++ 模板或内容规模。

## 2. Phase 2 范围

Phase 2 只覆盖三个基础模式：

1. Hash Map / Set
2. Two Pointers
3. Sliding Window

计划节奏：

- 每周完成 3 道新题。
- 每周复刷 2 道旧题。
- Phase 2 新增约 12 道题。
- 一个模式至少积累 3 道相关题后，才编写模式总结。

不在本阶段处理动态规划、图论、高阶树结构、竞赛模板或题库自动化。

### 2.1 题集来源与筛选

仓库新增一份 `algorithms/problem-set.md`，记录从 Algo-Atlas 路线中筛选出的代表题、来源链接、所属模式、难度、计划周次和完成状态。

采用 Algo-Atlas 的早期顺序：

> Hash Map 基线复盘 → Two Pointers → Sliding Window

现有 6 道 Hash Map 题作为基线，不重复计入 Phase 2 的 12 道新题。新题安排如下：

| 顺序 | 模式 | LeetCode | 题目 |
| --- | --- | --- | --- |
| 1 | Two Pointers | 283 | Move Zeroes |
| 2 | Two Pointers | 202 | Happy Number |
| 3 | Two Pointers | 167 | Two Sum II - Input Array Is Sorted |
| 4 | Two Pointers | 11 | Container With Most Water |
| 5 | Two Pointers | 15 | 3Sum |
| 6 | Two Pointers | 18 | 4Sum |
| 7 | Sliding Window | 209 | Minimum Size Subarray Sum |
| 8 | Sliding Window | 3 | Longest Substring Without Repeating Characters |
| 9 | Sliding Window | 1004 | Max Consecutive Ones III |
| 10 | Sliding Window | 904 | Fruit Into Baskets |
| 11 | Sliding Window | 1658 | Minimum Operations to Reduce X to Zero |
| 12 | Sliding Window | 438 | Find All Anagrams in a String |

`Happy Number` 同时可以用 Hash Set 解循环，本阶段将其放在 Two Pointers 中训练快慢指针，并在题目笔记中链接相关模式。题集只定义学习顺序，不预先创建空白题解，也不将未完成题目标记为学习证据。

## 3. 目录设计

```text
algorithms/
├── README.md
├── patterns/
│   ├── hash-map.md
│   ├── two-pointers.md
│   └── sliding-window.md
├── problems/
│   ├── hash-map/
│   ├── two-pointers/
│   └── sliding-window/
├── templates/
│   └── problem-note.md
└── review-log.md
```

### `README.md`

作为算法区域总入口，包含：

- 当前学习范围。
- 三个模式的导航。
- 题目清单和当前状态。
- 最近一次复刷结果。
- Phase 2 完成标准。

### `patterns/`

每个文件描述一种可迁移的解题模式，而不是重复单题答案。内容包括：

- 识别信号。
- 适用与不适用场景。
- 通用 Python 模板。
- 时间和空间复杂度。
- 常见错误。
- 代表题和相邻模式。

### `problems/`

保存单题记录，并按主要模式分类。一道题只选择一个主要目录；其他相关模式通过文档链接表达，避免重复文件。

### `review-log.md`

集中记录复刷结果，字段固定为：

| 日期 | 题目 | 模式 | 用时 | 是否独立完成 | 状态 | 下次复刷 | 主要问题 |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 4. 单题笔记规范

单题笔记只保留对面试训练有直接价值的字段：

1. 题目信息和主要模式。
2. 用自己的话复述输入、输出和约束。
3. 识别该模式的信号。
4. 第一次思路与卡点。
5. 最终解法和 Python 代码。
6. 时间、空间复杂度及理由。
7. 至少两个有效边界条件。
8. 本次错误和下一次复刷日期。
9. 一段可在面试中口头表达的解题说明。

不要求为了完整模板保留无法填写的空章节。某个字段没有信息时应删除或明确写出尚未理解的具体问题。

## 5. 状态模型

每道题只能处于以下一种状态：

- `learning`：尚不能独立完成。
- `review`：已经理解，但仍需提示或实现不稳定。
- `mastered`：在无提示条件下独立完成，并能解释模式与复杂度。

进入 `mastered` 必须同时满足：

1. 无提示独立写出正确实现。
2. 能解释为什么使用该模式。
3. 能正确分析时间和空间复杂度。
4. 能处理至少两个边界条件。

## 6. 学习工作流

```text
选择一道题
  → 限时独立尝试
  → 记录失败点或完成实现
  → 对照题解修正
  → 完成单题笔记
  → 更新 review-log
  → 同模式累计三题后更新 pattern 总结
  → 到期复刷
```

复刷时优先写代码和口头解释，不先阅读旧答案。复刷结果只更新 `review-log.md` 和必要的错误总结，避免复制新的重复笔记。

## 7. 现有内容迁移

现有 6 篇算法笔记作为首批素材：

- `001-two-sum.md`
- `002-contains-duplicate.md`
- `003-valid-anagram.md`
- `004-ransom-note.md`
- `005-group-anagrams.md`
- `006-top-k-frequent-elements.md`

迁移时：

1. 将文件放入 `problems/hash-map/`。
2. 保留用户已经写出的思考、错误和代码。
3. 删除纯占位内容，不替用户补写未掌握的结论。
4. 修复原索引中的文件路径。
5. 根据现有证据设置 `learning` 或 `review`，不能仅凭文件存在标记为 `mastered`。

## 8. 验收标准

Phase 2 算法模式库完成需要同时满足：

- 目录和导航可以从算法 `README.md` 一步访问。
- 三个模式各有一篇模式总结。
- Phase 2 新增约 12 道题，且每个模式至少 3 道。
- 每道题都有明确状态和复刷记录。
- 至少 6 道题完成一次无提示复刷。
- 至少 3 道题达到 `mastered`。
- 文档内部链接检查通过，不存在迁移造成的失效链接。

题目总数不是单独的完成证据；模式识别、独立实现和复刷结果才是主要验收依据。

## 9. 后续扩展边界

完成 Phase 2 后，根据实际薄弱点选择下一个模式，不能一次性创建所有空目录。算法内容达到约 30 题、至少 5 个稳定模式后，再评估是否从学习笔记仓库拆分成独立算法仓库。
