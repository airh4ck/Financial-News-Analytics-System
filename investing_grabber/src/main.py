import os
import time

import KafkaProducer
from json import load, dump

from CurrencyPair import CurrencyPair
from DatabaseUpdater import DatabaseUpdater
from InvestingOpinionsParser import InvestingOpinionsParser
from InvestingArticleParser import InvestingArticleParser


def updateDataset(currencyPair: CurrencyPair, latestArticle: int) -> None:
    articleParser = InvestingArticleParser()
    opinionsParser = InvestingOpinionsParser(articleParser)
    updater = DatabaseUpdater(opinionsParser)

    recentData = updater.getRecentData(currencyPair, latestArticle)

    KafkaProducer.uploadData(recentData)


def main():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../resources/latest_article.json')
    latestArticles = None
    with open(filename, "r") as latestArticlesFile:
        latestArticles = load(latestArticlesFile)

    if latestArticlesFile is None:
        print("Could not open file with latest articles info, shutting down")
        exit(1)

    for currencyPair in CurrencyPair:
        print(f'Updating {currencyPair.value} data...')
        try:
            updateDataset(currencyPair, latestArticles)
            print('Updated successfully!')
        except Exception as e:
            print(f'Update for {currencyPair.value} failed')
            print(e)

        with open(filename, "w") as latestArticlesFile:
            dump(latestArticles, latestArticlesFile)

        print(latestArticles)


if __name__ == "__main__":
    while True:
        start_time = time.time()
        main()
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(300)
