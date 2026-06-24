---
source_note: notes/library/python/basics/2026-05-24笔记：JSON.md
source_added_at: 2026-06-21T11:38:36+08:00
review_date: 2026-06-24
knowledge_point: JSON 的对象/数组结构与 Python 中 dumps/loads 的作用
new_or_old: new
review_round: 0
interval_days: 0
next_review_date: 2026-06-24
status: pending
---

## 1. 知识点与来源

- 知识点：JSON 对象与数组的基本结构，JSON 的格式特点，以及 Python 里 `json.dumps` / `json.loads` 的职责。
- 来源：`notes/library/python/basics/2026-05-24笔记：JSON.md`
- 定位范围：`JSON 对象`、`JSON数组`、`Python JSON`、`json.dumps` 相关段落。

## 2. 知识点盲测

1. 概念复述：这份笔记如何定义 JSON？它为什么适合做不同系统或语言之间的数据交换格式？
2. 辨析边界：JSON 对象和 JSON 数组在结构上分别长什么样？对象里的 `key` 有什么限制？
3. 实际应用：在 Python 里，`json.dumps` 和 `json.loads` 分别把什么转换成什么？
4. 易错点辨析：为什么笔记特别提醒 `ensure_ascii=False`？它主要是在什么场景下避免什么问题？

## 3. 我的作答区

1.
> JSON是一种轻量级的数据交换格式
2.
> 对象：{k:v,k:v}数组：["k",v]

3.
> json.dumps是转化成python字符串，json.load转换为python对象

4.
> 忘记了

## 4. 参考答案与易错点解析

<details>
<summary>展开查看参考答案与易错点</summary>

### 第 1 题

- 参考答案：笔记把 JSON 定义为一种轻量级的数据交换格式，用来在不同系统、程序、语言之间传递统一格式的数据。它轻量、可读、易解析、跨语言，所以适合交换数据。
- 常见误区：只记住“JSON 长得像字典”，却忘了它的核心用途是跨系统传输。
- 误区产生原因：平时常在单一语言环境里接触 JSON，不容易意识到它的交换格式属性。
- 正确判断线索：一提到前后端、接口、配置、模型输入输出，就要想到 JSON 的“统一格式”价值。

### 第 2 题

- 参考答案：JSON 对象写在 `{}` 中，由多个 `key: value` 组成；JSON 数组写在 `[]` 中，可以包含多个对象。对象里的 `key` 必须是字符串，`value` 可以是字符串、数字、对象、数组、布尔值或 `null`。
- 常见误区：把对象和数组的括号写混，或者以为对象的 key 可以随便用任意类型。
- 误区产生原因：在 Python 里字典 key 类型更灵活，容易把语言内对象规则带到 JSON 里。
- 正确判断线索：先看最外层括号，再确认对象键名是否是字符串。

### 第 3 题

- 参考答案：`json.dumps` 把 Python 对象编码成 JSON 字符串；`json.loads` 把已经编码好的 JSON 字符串解码成 Python 对象。
- 常见误区：把 `dumps` 和 `loads` 的方向记反，或者以为它们都是“打印 JSON”。
- 误区产生原因：两个函数名字相似，而且日常口语里“读/写 JSON”方向不够明确。
- 正确判断线索：记住 `dump` 更像“输出/编码”，`load` 更像“读入/解码”。

### 第 4 题

- 参考答案：笔记提醒 `ensure_ascii=True` 是中文处理里的常见坑，实际开发常写 `ensure_ascii=False`，这样可以避免中文被强制转成 ASCII 转义形式，提升可读性。
- 常见误区：以为 JSON 只要能序列化成功就行，不关心中文是否变成难读的转义内容。
- 误区产生原因：初学时更关注“能不能跑通”，忽略输出是否适合人读和调试。
- 正确判断线索：只要数据里可能出现中文，就主动检查 `ensure_ascii` 设置。

</details>

## 5. 复习结果

- 自评：`[ ] 掌握` `[x] 模糊` `[ ] 答错`
- 实际易错点：json定义遗忘、json实际用法模糊
- 完成时间：6.24
- 下次复习日期：

## 6. 下次复习建议

下次先口述“对象/数组/`dumps`/`loads` 四件事各自是什么”，再补一句为什么中文 JSON 往往会显式设置 `ensure_ascii=False`。
