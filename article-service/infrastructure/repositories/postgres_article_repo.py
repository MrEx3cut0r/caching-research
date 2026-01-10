import psycopg2
from typing import List, Optional
from domain.ports.article_repository import IArticleRepository
from domain.entities.article import Article

class PostgresArticleRepository(IArticleRepository):
    
    def __init__(self, connection_string: str = None):
        self.conn = psycopg2.connect(
            connection_string or 
            "host=postgres dbname=articles user=user password=password"
        )
    
    def find_by_id(self, article_id: str) -> Optional[Article]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, title, content, views FROM articles WHERE id = %s", (article_id,))
            row = cur.fetchone()
            if row:
                return Article(id=row[0], title=row[1], content=row[2], views=row[3])
        return None
    
    def save(self, article: Article) -> None:
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO articles (id, title, content, views) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE 
                SET title = EXCLUDED.title, 
                    content = EXCLUDED.content,
                    views = EXCLUDED.views
            """, (article.id, article.title, article.content, article.views))
            self.conn.commit()
    
    def get_popular(self, limit: int = 10) -> List[Article]:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, content, views 
                FROM articles 
                ORDER BY views DESC 
                LIMIT %s
            """, (limit,))
            rows = cur.fetchall()
            return [
                Article(id=row[0], title=row[1], content=row[2], views=row[3])
                for row in rows
            ]
    
    def close(self):
        if self.conn:
            self.conn.close()