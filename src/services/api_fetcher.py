from newsapi import NewsApiClient
from utils.dataclasses import Article
from typing import Optional, List, Dict
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
class APIFetcher:
    
    def __init__(self, api_key: str):
        self.client = NewsApiClient(api_key)
        try:
            response = self.client.get_sources()
            if response.get('status') != 'ok':
                logger.error("API недоступно или ключ недействителен")
                raise ValueError("API недоступно или ключ недействителен")
        except Exception as e:
            logger.error(f"Ошибка при подключении к API: {e}")
            raise
        
    async def fetch_articles(
        self,
        query: str,
        sources: Optional[List[str]] = None,
        domains: Optional[List[str]] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        language: str = 'ru',
        sort_by: str = 'publishedAt',
        page_size: int = 100
    ) -> List[Article]:
        
        try:
            logger.info(f"Запрос статей: query={query}, from_date={from_date}, to_date={to_date}")
            response = self.client.get_top_headlines(
                q=query if query else None,
                sources=','.join(sources) if sources else None,
                domains=','.join(domains) if domains else None,
                from_param=from_date.isoformat() if from_date else None,
                to=to_date.isoformat() if to_date else None,
                language=language,
                sort_by=sort_by,
                page_size=page_size
            )
            logger.info(f"Получено {len(response['articles'])} статей.")
            return [
                Article(
                    source=article['source']['name'],
                    author=article.get('author'),
                    title=article['title'],
                    description=article.get('description'),
                    url=article['url'],
                    url_to_image=article.get('urlToImage'),
                    published_at=datetime.fromisoformat(article['publishedAt']),
                    content=article.get('content')
                )
                for article in response['articles']
            ]
        except Exception as e:
            logger.error(f"Ошибка при получении статей: {e}")
            return []

    async def fetch_news(self) -> List[Dict]:
        try:
            logger.info("Fetching news")
            sources = [
                'lenta', 'ria', 'tass', 'rt', 'rbc', 'kommersant', 
                'gazeta', 'vedomosti', 'mk', 'rg'
            ]
            response = self.client.get_everything(
                sources=','.join(sources),
                language='ru',
                sort_by='publishedAt',
                page_size=100
            )
            
            logger.debug(f"API response: {response}")
            
            if response.get('status') != 'ok':
                logger.error(f"Ошибка API: {response.get('message', 'Unknown error')}")
                return []
            
            articles = response.get('articles', [])
            logger.info(f"Received {len(articles)} articles")
            return articles
        except Exception as e:
            logger.error(f"Ошибка при фетчинге новостей: {str(e)}", exc_info=True)
            return []
