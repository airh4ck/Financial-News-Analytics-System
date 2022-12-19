import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast


def create_tokenizer():
    return BertTokenizerFast.from_pretrained('blanchefort/rubert-base-cased-sentiment')


def create_model():
    return AutoModelForSequenceClassification.from_pretrained('blanchefort/rubert-base-cased-sentiment', return_dict=True)


@torch.no_grad()
def predict(text, tokenizer, model):
    inputs = tokenizer(text, max_length=512, padding=True,
                       truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmax(predicted, dim=1).numpy()
    return predicted
