# NumPy Transformer 第 1 周 Lab 构建计划

**目标：** 为“理论理解后自己实现”的第 1 周 Transformer Lab 建立脚手架、分关卡任务和隐藏核心 autograder；不在任何学习材料中提供函数实现代码。

**边界：** Lab 在 `projects/math-for-rag-labs/` 内独立创建，不修改已有的脏 notebook。学习者可见内容只包括题目、函数签名、公开冒烟测试和提示；真实答案与隐藏评分样例只留在评分器内部。

## 交付结构

| 路径 | 学习者是否可见 | 用途 |
| --- | --- | --- |
| `transformer_lab/README.md` | 是 | Lab 总览、运行方式、评分规则。 |
| `transformer_lab/lab.md` | 是 | 五关题目、理论前置、函数契约、提示与解锁条件。 |
| `transformer_lab/src/` | 是 | 仅含函数签名、docstring 和明确的未实现标记。 |
| `transformer_lab/tests/test_smoke.py` | 是 | 最小运行检查；不含关键边界样例。 |
| `transformer_lab/autograder/` | 否 | 隐藏输入、期望性质、评分逻辑和薄弱点报告。 |
| `transformer_lab/run_grade.py` | 是 | 只输出分数、失败类别和思考提示。 |

## 关卡设计

| 关卡 | 交付函数 | 理论前置 | hidden autograder 检查 | 失败反馈 |
| --- | --- | --- | --- | --- |
| 0 | 无 | token shape、矩阵乘法 | 环境、导入、签名 | “先检查 token 与权重矩阵的最后两维。” |
| 1 | `softmax(scores)` | 指数归一化、数值稳定性 | 每行归一化、极大/极小值、有限输出 | “检查减去最大值发生在 exp 前，及归一化轴。” |
| 2 | `scaled_dot_product_attention(q, k, v)` | Q/K/V、缩放、加权和 | shape、缩放、权重性质 | “检查 QK^T 的 shape、缩放项和 softmax 的轴。” |
| 3 | `causal_mask(length)`、`self_attention(...)` | 自回归、未来信息泄露 | 上三角屏蔽、长度 1、无 NaN | “mask 必须在 softmax 前影响 score。” |
| 4 | `layer_norm`、`ffn`、`transformer_block` | 残差、归一化、前向组合 | 组合顺序、输入不被修改、shape | “逐段打印 shape；确认残差两侧的维度相同。” |

## 实施任务

### 任务 1：题目与脚手架

- [ ] 创建 Lab 目录、README 和 `lab.md`。
- [ ] 对每关写明：理论阅读问题、函数签名、输入输出 shape、禁止事项、通过条件和至多三条渐进提示。
- [ ] 在 `src/` 只放函数签名和 docstring；函数调用时抛出明确的“请在本关实现此函数”错误。
- [ ] 提供一个只验证导入和函数存在的公开 smoke test，不透露关键数值样例。
- [ ] 验收：学习者可运行 smoke test，并知道从第 0 关开始。

### 任务 2：隐藏 autograder

- [ ] 为每关写独立的隐藏性质测试，不保存或打印期望数值。
- [ ] 将失败归入五类：`数值稳定性`、`shape/维度`、`mask 逻辑`、`组合顺序`、`边界输入`。
- [ ] 每个类别映射到一条机制提示和一个自检问题；输出中不包含隐藏样例、参考实现或具体期望矩阵。
- [ ] 设置门槛：当前关所有 P0 检查通过后才显示下一关“可开始”状态。
- [ ] 验收：故意放入错误实现时，评分器只报告类别与提示；正确实现时解锁下一关。

### 任务 3：薄弱点报告和学习证据

- [ ] `run_grade.py` 输出关卡状态、通过项数量、失败类别、下一步提示和“本次最该复习的概念”。
- [ ] 每关结束要求学习者记录：错误类别、自己的原因假设、验证方法和修复后理解。
- [ ] 第 4 关通过后生成第 2 周独立 demo 的入口清单：不得复制 Lab 解答；必须重新写出 block、训练和生成。
- [ ] 验收：一次完整评分可告诉学习者“哪里错了、应该思考什么”，但无法从输出反推出答案。

## 验证命令

在 `projects/math-for-rag-labs` 中运行：

```bash
uv run python transformer_lab/run_grade.py
uv run pytest transformer_lab/tests/test_smoke.py -v
```

预期：评分器输出当前关卡、失败类别或解锁状态；公开测试只验证脚手架能运行。

## 不做的事

- 不提供任何 softmax、attention、mask、LayerNorm、FFN 或 Transformer block 的实现答案。
- 不在第 1 周加入训练、字符生成、multi-head attention、PyTorch 或 RAG。
- 不修改既有 `notebooks/01-vector-similarity.ipynb`、`notes/library/` 或其他子模块。
- 未获用户明确授权，不提交或推送。
