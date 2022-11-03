import json
import summarize


def main():
    articleInfo = None
    with open("sample.json", 'r') as f:
        articleInfo = f.read()

    print(summarize.summarize(json.loads(articleInfo)["text"]))


if __name__ == "__main__":
    main()
