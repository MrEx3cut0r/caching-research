import redis
import json
import threading
from datetime import datetime
from queue import Queue
from domain.ports.cache_strategy import ICacheStrategy
from domain.entities.article import Article
from infrastructure.repositories.postgres_article_repo import PostgresArticleRepository

class WriteBehindStrategy(ICacheStrategy):
    def __init__(self, redis_host='redis', redis_port=6379, batch_size=10, flush_interval=5):
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.db = PostgresArticleRepository()
        self.write_queue = Queue()
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.flush_thread = threading.Thread(target=self._batch_writer, daemon=True)
        self.flush_thread.start()
    
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
        article_dict = article.__dict__.copy()
        article_dict['created_at'] = article_dict['created_at'].isoformat()
        self.redis.setex(f"article:{article.id}", 300, json.dumps(article_dict))
        self.write_queue.put(article)
    
    def _batch_writer(self):
        import time
        batch = []
        last_flush = time.time()
        
        while True:
            try:
                article = self.write_queue.get(timeout=1)
                batch.append(article)
                
                if len(batch) >= self.batch_size or (time.time() - last_flush) >= self.flush_interval:
                    for art in batch:
                        self.db.save(art)
                    batch.clear()
                    last_flush = time.time()
                    
            except Exception:
                if batch:
                    for art in batch:
                        self.db.save(art)
                    batch.clear()