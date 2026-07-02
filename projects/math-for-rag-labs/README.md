# Math for RAG Labs

这个目录用于保存 RAG、Transformer 和 LLM 工程相关数学基础的代码实验。

目标不是写一个独立数学教程，而是把 `notes/library/math-for-ai/` 中的概念用代码跑通，形成可复查的学习证据。

## 推荐环境

优先使用 VS Code Notebook 或 Jupyter Notebook。

最小依赖：

- Python 3.11+
- NumPy
- PyTorch
- Matplotlib，可选

## 环境配置

本目录使用 `uv` 管理 Python 环境，并固定使用 Python 3.12，避免系统 Python 版本影响 PyTorch。

第一次使用：

```bash
cd projects/math-for-rag-labs
uv sync
uv run python -m ipykernel install --user --name math-for-rag-labs-py312 --display-name "Python 3.12 (math-for-rag-labs)"
```

之后可以在 VS Code 或 Jupyter 中选择 kernel：

```text
Python 3.12 (math-for-rag-labs)
```

如果在 VS Code 里看到 `ModuleNotFoundError: No module named 'numpy'`，通常是 notebook 选错了 kernel。点击 notebook 右上角的 kernel 名称，切换到：

```text
Python 3.12 (math-for-rag-labs)
```

或者直接用 VS Code 打开这个目录，而不是只打开单个 `.ipynb` 文件：

```bash
code projects/math-for-rag-labs
```

验证环境：

```bash
uv run python -c "import numpy, torch; print(numpy.__version__); print(torch.__version__)"
```

## 实验规则

每个 notebook 尽量包含：

1. 概念说明
2. 一个手算小例子
3. NumPy 实现
4. PyTorch 实现
5. shape 检查
6. 和 RAG 或 Transformer 的关系
7. 一句话总结

## Notebook 计划

- [ ] `notebooks/01-vector-similarity.ipynb`
- [ ] `notebooks/02-softmax.ipynb`
- [ ] `notebooks/03-attention-score.ipynb`
- [ ] `notebooks/04-pytorch-tensor-shape.ipynb`
- [ ] `notebooks/05-embedding-layer.ipynb`

## 与主线项目的关系

这些实验最终服务于最小 RAG demo：

- 分块后文本会被表示成 embedding 向量
- query 和 chunk 通过相似度计算排序
- top-k 片段会进入 prompt
- attention 和 softmax 帮助理解 Transformer 如何处理上下文
