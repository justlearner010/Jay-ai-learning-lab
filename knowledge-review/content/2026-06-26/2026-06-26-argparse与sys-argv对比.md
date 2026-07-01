---
source_note: notes/library/python/basics/2026-05-25笔记：argparse.md
source_added_at: 2026-06-21T11:38:36+08:00
review_date: 2026-06-26
knowledge_point: argparse 相比 sys.argv 的优势，以及 add_argument 的基本角色
new_or_old: new
review_round: 0
interval_days: 0
next_review_date: 2026-06-26
status: pending
---

## 1. 知识点与来源

- 知识点：为什么 CLI 参数解析更推荐 argparse，以及位置参数和可选参数的基本写法。
- 来源：`notes/library/python/basics/2026-05-25笔记：argparse.md`
- 定位范围：`argparse` 作用、和 `sys.argv` 的对比、`add_argument()`、`--help` 相关段落。

## 2. 知识点盲测

1. 概念复述：这份笔记里 `argparse` 被定义成什么工具？它主要替你处理哪类任务？
2. 辨析边界：和直接读取 `sys.argv` 相比，`argparse` 至少在哪三件事上更强？
3. 实际应用：`parser.add_argument("fname")` 和 `parser.add_argument("--size")` 分别表示什么样的参数？

## 3. 我的作答区

1.
>

2.
>

3.
>

## 4. 参考答案与易错点解析

<details>
<summary>展开查看参考答案与易错点</summary>

### 第 1 题

- 参考答案：`argparse` 是 Python 标准库中专门解析命令行参数的模块，用来自动读取参数、做类型转换、生成 `--help`，并检查参数是否合法。
- 常见误区：把 `argparse` 只理解成 `sys.argv` 的语法糖。
- 误区产生原因：两者都处理命令行参数，表面上看像替代品。
- 正确判断线索：只要需求里出现帮助文档、类型检查或参数校验，就想到 `argparse`。

### 第 2 题

- 参考答案：笔记里强调的优势至少有三点：参数缺失时给出更清晰的错误信息、支持自动类型检查、能自动生成 `--help` 帮助文档。
- 常见误区：只记住 `argparse` 更高级，却说不出具体高级在哪。
- 误区产生原因：没有把“程序员手写校验”和“库自动完成”对应起来。
- 正确判断线索：回忆 `IndexError`、`invalid int value`、`usage: ...` 这三个典型场景。

### 第 3 题

- 参考答案：`add_argument("fname")` 表示必填的位置参数；`add_argument("--size")` 表示带名字的可选参数，调用时通常写成 `--size 100`。
- 常见误区：把带 `--` 的参数也当成普通位置参数，或忘记调用时要显式写名称。
- 误区产生原因：命令行参数的“位置”和“命名”两套风格容易混淆。
- 正确判断线索：没有 `--` 的通常按位置传，有 `--` 的需要带着名字传。

</details>

## 5. 复习结果

- 自评：`[ ] 掌握` `[ ] 模糊` `[ ] 答错`
- 实际易错点：
- 完成时间：
- 下次复习日期：

## 6. 下次复习建议

下次先不看答案，直接说出 `argparse` 相比 `sys.argv` 多做了哪三件事，再写一遍位置参数和可选参数的最小示例。
