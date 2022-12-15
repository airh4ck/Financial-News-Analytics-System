from typing import List, Dict
import re

from pandas import DataFrame
from CurrencyPair import CurrencyPair
from OpinionsParser import OpinionsParser


class DatabaseUpdater():
    def __init__(self, opinionsParser: OpinionsParser):
        self.__opinionsParser = opinionsParser
        self.__currency_pair = {
            CurrencyPair.EURUSD: 'eur_usd',
            CurrencyPair.GBPUSD: 'gbp_usd',
            CurrencyPair.AUDUSD: 'aud_usd',
            CurrencyPair.GBPJPY: 'gbp_jpy',
            CurrencyPair.USDCAD: 'usd_cad',
            CurrencyPair.USDCHF: 'usd_chf',
            CurrencyPair.USDJPY: 'usd_jpy',
            CurrencyPair.EURGBP: 'eur_gbp'
        }

    def getRecentData(self, currencyPair: CurrencyPair, latestArticles: Dict[str, int]) -> List[Dict[str, str]]:
        page = 1
        result = list()

        breakFlag = False
        latestArticle = latestArticles[currencyPair.value]

        newLatestArticle = latestArticle
        while not breakFlag:
            link = "https://ru.investing.com/currencies/" + \
                currencyPair.value + "-opinion/" + \
                (str(page) if page > 1 else "")

            for entry in self.__opinionsParser.parsePage(link):
                if int(re.findall(r'\d+', entry['link'])[0]) <= latestArticle:
                    breakFlag = True
                else:
                    entry['pair'] = self.__currency_pair[currencyPair]
                    result.append(entry)

                    if newLatestArticle == latestArticle:
                        newLatestArticle = int(
                            re.findall(r'\d+', entry['link'])[0])

            page += 1

        latestArticles[currencyPair.value] = newLatestArticle
        return result
