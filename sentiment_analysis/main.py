import JSONParse
import analyze


def main():
    # TODO Integrate with Apache Kafka
    articleInfo = None
    with open("sample.json", 'r') as f:
        articleInfo = f.read()

    # TODO send the result to the database
    print(analyze.predict(JSONParse.getArticleFrom(articleInfo)))


if __name__ == "__main__":
    main()
