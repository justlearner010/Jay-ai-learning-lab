
``` 
Stage 1: CLI System
  → text pipeline + modular design

Stage 2: RAG System
  → knowledge pipeline + retrieval

Stage 3: Tool Agent
  → planner + tool executor

Stage 4: Coding Agent
  → self-debug + code loop

Stage 5: Learning OS
  → meta task system + feedback loop
```


## ① CLI 是否可长期维护

- 有没有 test
- 有没有结构
- 有没有扩展接口

---

## ② RAG 是否稳定复现

- 同样输入 → 是否稳定输出

---

## ③ Agent 是否能闭环执行任务

- 不是 demo
- 是“多步任务完成能力”

---

如果这三层没闭环，OS层就是空的。