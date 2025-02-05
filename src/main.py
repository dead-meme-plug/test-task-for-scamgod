import asyncio
import logging
from aiogram.fsm.storage.memory import MemoryStorage

from src.core.config.config import BotConfig
from src.bot.bot import TGBot
from src.services.api_fetcher import APIFetcher
from src.services.news_fetcher import NewsFetcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    config = BotConfig("src/core/config/config.toml")
    bot = TGBot(config.telegram_bot_token)
    api_fetcher = APIFetcher(config.newsapi_key)
    news_fetcher = NewsFetcher(api_fetcher, bot.bot)
    asyncio.create_task(news_fetcher.start())
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
