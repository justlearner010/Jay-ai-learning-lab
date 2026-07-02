
### LLM Tokenization

prompt -> tokenizer

**tokenizer** breaks it into pieces

declare our prompt ,then tokenize it, then pass those tokens to the model, which generates its output.

Input -> Tokens ->Token IDs -> LLM 

space characters are not explicitly stored as separate tokens; instead ,tokens encode whether they begin with a space via a **hidden marker.**

#### **How it knows "word vs subword"**?

**byte pair encoding (BPE)**

The tokenizer builds a **fixed vocabulary of subword units**

Some tokens are learned as:

- full words: `"cat"`
- prefixes/suffixes: `"izing"`, `"ic"`
- punctuation pieces, etc.

Then a **special marker**(like a leading space or Ġ) encodes boundary information

- `"cat"` → token that appears at word start
- `"Ġcat"` → token that starts with a space → means “new word starts here”

P67 - 2026.7.1
