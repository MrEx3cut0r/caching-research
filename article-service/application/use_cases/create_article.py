from domain.entities.article import Article
from domain.ports.cache_strategy import ICacheStrategy

class CreateArticleUseCase:
    def __init__(self, cache_strategy: ICacheStrategy):
        self.cache_strategy = cache_strategy
    
    def execute(self, title: str, content: str) -> Article:
        article_id = Article.generate_id(title, content)
        article = Article(
            id=article_id,
            title=title,
            content=content,
            views=0
        )
        self.cache_strategy.save_article(article)
        return article