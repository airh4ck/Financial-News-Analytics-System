from ctypes import ArgumentError
from typing import List, Dict

import re
from cloudscraper import create_scraper
from bs4 import BeautifulSoup

from ArticleParser import ArticleParser
from OpinionsParser import OpinionsParser


class InvestingOpinionsParser(OpinionsParser):
    def __init__(self, articleParser: ArticleParser):
        self.__articleParser = articleParser
        self.__INVESTING_URL = "https://ru.investing.com"

    def parsePage(self, link: str) -> List[Dict[str, str]]:
        if not link.startswith("https://ru.investing.com/currencies/"):
            raise ArgumentError(
                "Link parameter should be a link to investing.com website")

        result = list(list())

        scraper = create_scraper()

        parsedHtml = BeautifulSoup(scraper.get(
            link).text, features="html.parser")
        for articleLink in self.__getArticlesFromPage(parsedHtml):
            try:
                articleHtml = scraper.get(
                    self.__INVESTING_URL + articleLink).text
                parsedArticle = self.__articleParser.parseArticle(
                    BeautifulSoup(articleHtml, features="html.parser"))

                parsedArticle['link'] = self.__INVESTING_URL + articleLink
                result.append(parsedArticle)
            except:
                pass

        return result

    def __getArticlesFromPage(self, parsedHtml: BeautifulSoup) -> List[str]:
        links = set()

        for link in parsedHtml.findAll("a", attrs={'href': re.compile(r'/analysis/article-[0-9]+$')}):
            links.add(link.get('href'))

        return list(links)
