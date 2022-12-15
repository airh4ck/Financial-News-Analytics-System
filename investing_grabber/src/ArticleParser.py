from abc import abstractmethod
from typing import Dict

from bs4 import BeautifulSoup

class ArticleParser:
	@abstractmethod
	def parseArticle(self, parsedArticle: BeautifulSoup) -> Dict[str, str]:
		pass