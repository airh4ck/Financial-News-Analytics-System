import json


def getArticleFrom(input) -> str:
    return json.loads(input)['text']
