from typing import Optional
from domain.entities.article import Article
from domain.ports.cache_strategy import ICacheStrategy

class GetArticleUseCase:
    def __init__(self, cache_strategy: ICacheStrategy):
        self.cache_strategy = cache_strategy
    
    def execute(self, article_id: str) -> Optional[Article]:
        article = self.cache_strategy.get_article(article_id)
        if article:
            article.increment_views()
        return article