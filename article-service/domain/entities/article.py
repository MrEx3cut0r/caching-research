from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    id: str
    title: str
    content: str
    views: int = 0
    created_at: datetime = datetime.now()
    
    def increment_views(self):
        self.views += 1