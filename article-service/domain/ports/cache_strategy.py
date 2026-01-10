from abc import ABC, abstractmethod
from typing import Optional
from ..entities.article import Article

class ICacheStrategy(ABC):
    @abstractmethod
    def get_article(self, article_id: str) -> Optional[Article]:
        pass
    
    @abstractmethod
    def save_article(self, article: Article) -> None:
        pass