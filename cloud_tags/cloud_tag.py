from wordcloud import WordCloud


def create_cloud_tags(texts: list[str]) -> WordCloud:
    return WordCloud.generate(" ".join(texts))
