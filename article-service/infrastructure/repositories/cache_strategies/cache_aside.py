import redis
import json
from datetime import datetime
from domain.ports.cache_strategy import ICacheStrategy
from domain.entities.article import Article
from infrastructure.repositories.postgres_article_repo import PostgresArticleRepository

class CacheAsideStrategy(ICacheStrategy):
    def __init__(self, redis_host='redis', redis_port=6379):
        try:
            self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True, socket_connect_timeout=1, socket_timeout=1)
            self.redis.ping()
        except:
            self.redis = None
        
        try:
            self.db = PostgresArticleRepository()
        except:
            self.db = MockRepository()
    
    def get_article(self, article_id):
        if self.redis:
            cached = self.redis.get(f"article:{article_id}")
            if cached:
                try:
                    data = json.loads(cached)
                    if 'created_at' in data:
                        data['created_at'] = datetime.fromisoformat(data['created_at'])
                    return Article(**data)
                except:
                    pass
        
        article = self.db.find_by_id(article_id)
        if article and self.redis:
            try:
                article_dict = article.to_dict()
                self.redis.setex(f"article:{article_id}", 300, json.dumps(article_dict))
            except:
                pass
        return article
    
    def save_article(self, article):
        self.db.save(article)
        if self.redis:
            try:
                self.redis.delete(f"article:{article.id}")
            except:
                pass

class MockRepository:
    def __init__(self):
        self.data = {}
    
    def find_by_id(self, article_id):
        return self.data.get(article_id)
    
    def save(self, article):
        self.data[article.id] = article