import redis
from domain.ports.cache_strategy import ICacheStrategy
from domain.entities.article import Article
from ..postgres_article_repo import PostgresArticleRepository

class WriteThroughStrategy(ICacheStrategy):    
    def __init__(self):
        self.redis = redis.Redis(host='redis', port=6379)
        self.db = PostgresArticleRepository()
    
    def get_article(self, article_id: str):
        cached = self.redis.get(f"article:{article_id}")
        return Article(**eval(cached)) if cached else None
    
    def save_article(self, article: Article):
        self.db.save(article)
        self.redis.setex(
            f"article:{article_id}",
            300,
            str(article.__dict__)
        )

