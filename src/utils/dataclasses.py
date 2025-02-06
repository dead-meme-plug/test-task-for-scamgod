from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class Article:
    source: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    url_to_image: Optional[str]
    published_at: datetime
    content: Optional[str]