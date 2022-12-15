from bs4 import BeautifulSoup
from ArticleParser import ArticleParser
import re
from typing import Dict


class InvestingArticleParser(ArticleParser):
    def __init__(self) -> None:
        self.__parsedHtml: BeautifulSoup = None
        self.__contentDetails: BeautifulSoup = None

    def __setUp(self, parsedHtml: BeautifulSoup) -> None:
        for lineBreak in parsedHtml.findAll('br'):
            lineBreak.replaceWith('\n')

        self.__parsedHtml = parsedHtml
        self.__contentDetails = parsedHtml.find(
            "div", attrs={'class': 'contentSectionDetails'})

    def parseArticle(self, parsedHtml: BeautifulSoup) -> Dict[str, str]:
        self.__setUp(parsedHtml)

        return {
            'title': self.__parseTitle(),
            'author': self.__parseAuthor(),
            'date': self.__parseDate(),
            'time': self.__parseTime(),
            'text': self.__parseArticleText()
        }

    def __parseTitle(self) -> str:
        return self.__parsedHtml.find("h1", attrs={'class': 'articleHeader'}).get_text()

    def __parseAuthor(self) -> str:
        return self.__contentDetails.find("i").get_text()

    def __parseDate(self) -> str:
        date: str = None
        for span in self.__contentDetails.findAll('span'):
            if re.search(r'(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d', span.text) != None:
                date = re.search(
                    r'(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d', span.text).group(0)

        return date

    def __parseTime(self) -> str:
        time: str = None
        for span in self.__contentDetails.findAll('span'):
            if re.search(r'([0-1]?[0-9]|2[0-3]):[0-5][0-9]', span.text) != None:
                time = re.search(
                    r'([0-1]?[0-9]|2[0-3]):[0-5][0-9]', span.text).group(0)

        return time

    def __parseArticleText(self) -> str:
        articleText = self.__parsedHtml.find(
            "div", attrs={'class': 'WYSIWYG articlePage'})
        articleText.find(
            "div", attrs={'class': 'relatedInstrumentsWrapper'}).extract()

        return articleText.get_text()
