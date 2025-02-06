import asyncio
import logging
import sys

from core.config.config import BotConfig
from bot.bot import TGBot
from services.api_fetcher import APIFetcher
from services.news_fetcher import NewsFetcher
from core.database.db import init_db, close_db

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
    await config.load()
    await init_db(config)
    api_fetcher = APIFetcher(config.newsapi_key)
    bot = TGBot(config.telegram_bot_token, api_fetcher)
    
    try:
        await bot.start()
    finally:
        await bot.stop() 
        await close_db()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.run(close_db())