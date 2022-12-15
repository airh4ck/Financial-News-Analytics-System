from abc import abstractmethod
from typing import List, Dict


class OpinionsParser:
    @abstractmethod
    def parsePage(self, link: str) -> List[Dict[str, str]]:
        pass
