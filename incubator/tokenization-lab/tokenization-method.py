from transformers import AutoTokenizer

texts = [
    "我想学习AI",
    "Hello,world",
    "I Love Large Language Models",
    "我正在学习Tokenization Method",
]

models = [
    "bert-base-uncased",
    "gpt2",
    "google-t5/t5-small",
]

for model_name in models:
    print("=" * 80)
    print("MODEL:",model_name)

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    for text in texts:
        encoded = tokenizer(text)

        print("\nTEXT",text)
        print("TOKENS:", tokenizer.tokenize(text))
        print("IDS:", encoded["input_ids"])
        print("DECODED:", tokenizer.decode(encoded["input_ids"]))