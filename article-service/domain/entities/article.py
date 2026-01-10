from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Article:
    id: str
    title: str
    content: str
    views: int = 0
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        elif isinstance(self.created_at, str):
            try:
                self.created_at = datetime.fromisoformat(self.created_at.replace('Z', '+00:00'))
            except:
                self.created_at = datetime.now()
    
    def increment_views(self):
        self.views += 1
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'views': self.views,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def generate_id(title: str, content: str) -> str:
        return str(uuid.uuid4())