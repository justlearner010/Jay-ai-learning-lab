
这个 roadmap 用来记录我的阶段性学习路线。

它不是每日任务表，而是项目进度图。  
每个阶段都要产出可见成果，比如 README、项目卡片、测试、代码、复盘记录。

## 0. 总目标

把我的学习过程从零散任务，改造成一个可持续迭代的学习系统。

目标是让每一次学习都尽量沉淀为：

- 项目
- 笔记
- 测试
- README 文档
- 周复盘
- 可展示成果

最终希望形成一个清晰的 CS / AI Agent 学习资产库。

---

## 1. 当前优先级

当前最重要的三件事：

1. 重构 GitHub 仓库结构
2. 打磨 [`ai_reader`](https://github.com/justlearner010/ai_reader) 项目展示
3. 构建 [`textlab-cli`](https://github.com/justlearner010/jay-first-cli-text-tool) 作为 Python 工程化项目

暂时不追求开很多新坑，优先把已有成果整理清楚。

---

## Phase 1: GitHub 学习系统重构

### 目标

把原本零散的学习材料、作业、项目记录，整理成一个清晰的学习系统仓库。

### 主要任务

- [x] 建立`cs-learning-lab`仓库结构
- [x] 创建`projects/`
- [x] 创建`notes/`
- [x] 创建`logs/`
- [x] 创建 `templates/`
- [x] 创建`to do list`
- [x] 把旧计划、旧作业、原始记录移动到 `archive/`
- [x] 写好仓库 `README.md`
- [x] 写第一篇 weekly review

---
## Phase 2: Python文本CLI工具迭代与算法模版和Linux- CSAPP学习的初步构建

- [x] 为CLI工具加入更多边界条件测试
- [x] 加入选定单词的词频统计功能，做成CLI的-- 格式的命令行工具调用
- [x] 研究CLI工具的CLI化，将它变得更加工程化，将这个项目看为未来RAG项目的一个文本处理部分
- [ ] Linux - CSAPP仓库构建：初步定为：Linux学习 、CSAPP学习，具体结构待定
- [x] 建设[面试算法模式库](./notes/library/algorithms/README.md)：复刷 6 道 Hash Map 基线题，新增 6 道 Two Pointers 和 6 道 Sliding Window；每周完成 3 道新题和 2 道无提示复刷

---
## Phase3:补足RAG所需的前置基础知识
### 目标

不是泛泛补完数学、PyTorch 或 Transformer，而是补足能理解和实现最小 RAG demo 的前置能力。

完成标准：

- 能解释 RAG 为什么需要分块、embedding、向量相似度检索和上下文增强生成
- 能用 PyTorch 读懂 tensor、embedding、attention 的基本计算过程
- 能完成一个小型 RAG demo，并写清楚它的输入、处理流程、局限和失败案例

### 前半段：RAG 前置基础

#### 数学最小基础

- [ ] 向量与矩阵：理解向量、矩阵、矩阵乘法、转置、维度变化
- [ ] 向量相似度：理解 dot product、cosine similarity，以及它们为什么能用于检索
- [ ] 概率与归一化：理解概率分布、logits、softmax 的直觉
- [ ] 线性变换直觉：理解 embedding 向量空间和线性层的输入输出关系
- [ ] 产出一篇笔记：`notes/library/math-for-ai/RAG 需要哪些数学基础`

#### PyTorch 最小基础

- [ ] Tensor 基础：创建 tensor、查看 shape、索引、切片、广播和矩阵运算
- [ ] Autograd 基础：理解 `requires_grad`、反向传播和参数更新
- [ ] Module 基础：会写一个最小 `nn.Module`，理解 forward 的作用
- [ ] Dataset/DataLoader 基础：能把文本样本包装成可迭代数据
- [ ] Embedding 层小实验：用 `nn.Embedding` 观察 token id 到向量的映射
- [ ] 产出一个小 notebook 或脚本：`projects/math-for-rag-labs/notebooks/pytorch-basics-for-rag`

#### Transformer 最小基础

- [ ] Tokenization：理解文本如何变成 token id
- [ ] Embedding：理解 token embedding 和 position embedding 的作用
- [ ] Attention：能解释 query、key、value 和 attention score 的计算直觉
- [ ] Context window：理解上下文长度限制，以及为什么 RAG 要把外部资料塞进 prompt
- [ ] Encoder / decoder / decoder-only：理解三类结构的基本差别，不追求从零训练模型
- [ ] 产出一篇笔记：`notes/library/math-for-ai/Transformer 与 RAG 的关系`

### 后半段：最小 RAG demo

- [ ] 选择一个小型文档集：优先使用自己的 markdown 笔记或 `textlab-cli` 处理后的文本
- [ ] 完成文档分块：记录 chunk size、overlap 和分块失败案例
- [ ] 完成 embedding 与向量存储：可以先用本地文件或轻量向量库，不追求复杂架构
- [ ] 完成相似度检索：输入问题后返回 top-k 相关片段
- [ ] 完成生成问答：把检索片段放进 prompt，生成带来源引用的回答
- [ ] 增加最小测试：至少覆盖分块、检索和空结果处理
- [ ] 写 README：说明项目目标、运行方式、架构流程、已知局限和下一步
- [ ] 写一次复盘：记录哪些基础知识真正用上了，哪些只是暂时不需要
