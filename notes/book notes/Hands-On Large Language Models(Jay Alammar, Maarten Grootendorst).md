

# Reading Chapter

### #1 An introduction to Large Language Models

**The most common method for tokenization is by splitting on a whitespace to create individual word.**
Difference: Mandarin VS English
Mandarin doesn't have whitespaces around individual words
which will  be encompassed in Chapter2

What is the meaning of **tokenization**?

Split input by a whitespace
|
|
-> Vector representation

**embedding** :vector representations of data that attempt to capture its meaning

For example, **word2vec** generates word embeddings by looking at which other words they tend to appear next ot in a given sentence(**Prediction**)

Three layers:
|->**Input layer**
|
|-> **Hidden layer**
|
|->**Output layer**

**Chapter2**: look closer at word2vec's training procedure

embeddings in n-dimensional space

**RNN**?:  encoding or representing an input sentence and decoding or generating an output sentence.

**Autoregressive** : Each output token is used as input to generate next token
#### Attention
[**Attention**](https://arxiv.org/abs/1409.0473):**Chapter3** will go more in depth on the attention mechanism

Attention selectively determines which words are the most important in a given sentence

[Attention Is All You Need](https://oreil.ly/KGvIj)

**Transformer**:
|->Input Sequence

|->Transformer_Transformer encoder
		   |_ Transformer decoder
|->Output Sequence

Transformer consists of two parts,**self-attention** and a **feedforward neutral network**
#### MLM: Masked Language Modeling
**masked language modeling** ?

Example:

> Input: “The capital of France is [MASK].”
> Target: “Paris”

**Pretraining** and **Fine-tune**


Pretraining in my point of view is let a model input massive text data without labels, and let it generates labels automatically.The task of pretraining is to let model predict masked tokens

**It is self-supervised learning**

Fine-tune happens after pretraining.You take the pretrained model and continue training it on a specific downstream task with labeled data

Pretraining: Let model **know** the information
Fine-tune: Let model solve **concrete, defined application task**

#### Generative Models: Decoder-Only Models

Generatie Pre-trained Transformer:GPT, the origin of the name **ChatGPT**

GPT-1:

Input Sequence
|
_ Transformer:decoder
|
_ Next generated word

***Why GPT is a decoder-only model***:
- GPT is general-purpose text continuation
- it just need to predict the next token given all previous tokens

***Why decoder-only fits autoregressive generation?***

***What the difference between encoder-only models and decoder-only models***

These generative decoder-only models, especially the  "larger" models, are commonly referred to as *large language models* **(LLMs)**

User query -> Generative LLM -> Output

**foundation models** : The open source base models



### Some questions may in Chapter 2

- What is token
- What is embedding
- How can a word be a vector
- the n-dimensions, what is the definition of dimensions?
-
