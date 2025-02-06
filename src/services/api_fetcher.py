from newsapi import NewsApiClient
from utils.dataclasses import Article
from typing import Optional, List, Dict
from datetime import datetime
import logging
from services.text_analyzer import TextAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
class APIFetcher:
    
    def __init__(self, api_key: str, text_analyzer: TextAnalyzer):
        self.client = NewsApiClient(api_key)
        self.text_analyzer = text_analyzer
        try:
            response = self.client.get_sources()
            if response.get('status') != 'ok':
                logger.error("API недоступно или ключ недействителен")
                raise ValueError("API недоступно или ключ недействителен")
        except Exception as e:
            logger.error(f"Ошибка при подключении к API: {e}")
            raise

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
            
            for article in articles:
                text = article["title"] + " " + (article.get("content", "") or "")
                article["topics"] = self.text_analyzer.extract_topics(text)
            return articles
        except Exception as e:
            logger.error(f"Ошибка при фетчинге новостей: {str(e)}", exc_info=True)
            return []
