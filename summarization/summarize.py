from transformers import MBartTokenizer, MBartForConditionalGeneration

model_name = "IlyaGusev/mbart_ru_sum_gazeta"

def create_tokenizer():
    return MBartTokenizer.from_pretrained(model_name)

def create_model():
    return MBartForConditionalGeneration.from_pretrained(model_name)

def summarize(article_text, tokenizer, model):
    input_ids = tokenizer(
        [article_text],
        max_length=600,
        truncation=True,
        return_tensors="pt",
    )["input_ids"]

    output_ids = model.generate(
        input_ids=input_ids,
        no_repeat_ngram_size=4
    )[0]

    summary = tokenizer.decode(output_ids, skip_special_tokens=True)
    return summary