import asyncio
import logging
import sys

from core.config.config import BotConfig
from bot.bot import TGBot
from services.api_fetcher import APIFetcher
from services.news_fetcher import NewsFetcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def change_event_loop():
    if sys.platform == "win32":
        import winloop
        winloop.install()
        logger.info("Используется winloop")

async def main():
    change_event_loop()
    config = BotConfig("src/core/config/config.toml")
    bot = TGBot(config.telegram_bot_token)
    api_fetcher = APIFetcher(config.newsapi_key)
    news_fetcher = NewsFetcher(api_fetcher, bot.bot)
    asyncio.create_task(news_fetcher.start())
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
