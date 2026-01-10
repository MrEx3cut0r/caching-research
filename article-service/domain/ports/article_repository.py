from abc import ABC, abstractmethod
from typing import Optional
from ..entities.article import Article

class IArticleRepository(ABC):
    @abstractmethod
    def find_by_id(self, article_id: str) -> Optional[Article]:
        pass
    
    @abstractmethod
    def save(self, article: Article) -> None:
        pass
    
    @abstractmethod
    def get_popular(self, limit: int = 10) -> list[Article]:
        pass