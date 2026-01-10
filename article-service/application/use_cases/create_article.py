from domain.entities.article import Article
from domain.ports.cache_strategy import ICacheStrategy

class CreateArticleUseCase:
    
    def __init__(self, cache_strategy: ICacheStrategy):
        self.cache_strategy = cache_strategy
    
    def execute(self, title: str, content: str) -> Article:
        article = Article(
            id=str(hash(title + content)),
            title=title,
            content=content
        )
        self.cache_strategy.save_article(article)
        return article