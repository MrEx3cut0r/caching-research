import redis
import json
from datetime import datetime
from domain.ports.cache_strategy import ICacheStrategy
from domain.entities.article import Article
from infrastructure.repositories.postgres_article_repo import PostgresArticleRepository

class CacheAsideStrategy(ICacheStrategy):
    def __init__(self, redis_host='redis', redis_port=6379):
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.db = PostgresArticleRepository()
    
    def get_article(self, article_id):
        cached = self.redis.get(f"article:{article_id}")
        if cached:
            data = json.loads(cached)
            data['created_at'] = datetime.fromisoformat(data['created_at'])
            return Article(**data)
        
        article = self.db.find_by_id(article_id)
        if article:
            article_dict = article.__dict__.copy()
            article_dict['created_at'] = article_dict['created_at'].isoformat()
            self.redis.setex(f"article:{article_id}", 300, json.dumps(article_dict))
        return article
    
    def save_article(self, article):
        self.db.save(article)
        self.redis.delete(f"article:{article.id}")