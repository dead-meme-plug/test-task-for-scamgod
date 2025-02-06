from datetime import datetime, timedelta
import asyncio
import logging
from core.database.models import Article, Subscription, BotState
from services.api_fetcher import APIFetcher
from typing import List, Dict
from services.text_analyzer import TextAnalyzer

logger = logging.getLogger(__name__)

class NewsFetcher:
    def __init__(self, api_fetcher: APIFetcher, bot):
        self.api_fetcher = api_fetcher
        self.bot = bot
        self._task = None
        self.text_analyzer = TextAnalyzer()

    async def start(self, interval_minutes: int = 15):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._run(interval_minutes))

    async def stop(self):
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run(self, interval_minutes: int):
        while True:
            try:
                await self._fetch_and_process_news()
            except asyncio.CancelledError:
                logger.info("NewsFetcher остановлен")
                break
            except Exception as e:
                logger.error(f"Ошибка при фетчинге новостей: {e}")
            await asyncio.sleep(interval_minutes * 60)

    async def _fetch_and_process_news(self):
        articles = await self.api_fetcher.fetch_news()
        if articles:
            await self._process_articles(articles)

    async def _process_articles(self, articles: List[Dict]):
        logger.info(f"Processing {len(articles)} new articles")
        await self._save_articles(articles)
        await self._notify_users(articles)
        await self._save_last_fetch_time(datetime.now())

    async def _save_articles(self, articles: List[Dict]):
        for article in articles:
            topics = self.text_analyzer.extract_topics(article["title"] + " " + (article["content"] or ""))
            await Article.create(
                title=article["title"],
                content=article["content"],
                source=article["source"],
                url=article["url"],
                published_at=article["publishedAt"],
                topics=topics
            )

    async def _notify_users(self, articles: List[Dict]):
        for article in articles:
            subscriptions = await Subscription.filter(topic__in=article["topics"], is_active=True).prefetch_related("user")
            for subscription in subscriptions:
                await self.bot.send_message(
                    chat_id=subscription.user.id,
                    text=f"Новая статья по вашей подписке '{subscription.topic}':\n\n{article['title']}\n{article['url']}"
                )

    async def _load_last_fetch_time(self) -> datetime:
        state = await BotState.get_or_none(key="last_fetch_time")
        if state:
            return datetime.fromisoformat(state.value)
        return datetime.now() - timedelta(days=1)

    async def _save_last_fetch_time(self, time: datetime):
        await BotState.update_or_create(
            key="last_fetch_time",
            defaults={"value": time.isoformat()}
        )