from transformers import MBartTokenizer, MBartForConditionalGeneration


def summarize(articleText: str) -> str:
    modelName = "IlyaGusev/mbart_ru_sum_gazeta"
    tokenizer = MBartTokenizer.from_pretrained(modelName)
    model = MBartForConditionalGeneration.from_pretrained(modelName)

    inputIDs = tokenizer(
        [articleText],
        max_length=600,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )["input_ids"]

    outputIDs = model.generate(
        input_ids=inputIDs,
        no_repeat_ngram_size=4
    )[0]

    summary = tokenizer.decode(outputIDs, skip_special_tokens=True)
    return summary
