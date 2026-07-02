
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

P76 - 2026.7.1

- Subword tokens
- Word tokens
- Character tokens
- Byte tokens

Subword tokens present an advantage over character tokens in the ability to fit more text within the limited context length of a Transformer model

**BERT Base Model(uncased)(2018)**

cased: information priority
uncased: semantic meaning priority

Tokenization method :WordPiece
text
 ↓
tokenizer
 ↓
mapping to the 30k word lists
 ↓
add special token flags：
    [CLS] + [SEP] + [PAD] + [UNK]
 ↓
pass to Transformer

- UNK : Unknown token that the tokenizer has no specific encoding for
- SEP : A separator that enables certain tasks that require giving the model two texts 
- PAD :A padding token used to pad unused positions in the model's input
- CLS :A special classification token for classification tasks
- MASK : A masking token used to hide tokens during the training process

**BERT Base Model(cased)(2018)**

Tokenization method :WordPiece

**Question:What "lowercase" actually do?**

It  makes an information reduction or feature reduction

e.g:
{Apple, APPLE, apple}
          ↓
        apple

It is a many-to-one mapping, which reduces orthographic information and surface form.


**GPT-2(2019)**

Tokenization method: Byte pair encoding (BPE), 

BPE: Use a single byte based on frequency to composed of a pair

```
START: character level
"lower", "lowest"

l o w
l o w e r
l o w e s t


STEP 1: count most frequent adjacent pairs
("l","o"), ("lo","w"), ("e","r") ...


STEP 2: merge MOST FREQUENT pair

Example:
l + o → lo
lo + w → low
e + r → er


RESULT:
low + er
low + est
```

