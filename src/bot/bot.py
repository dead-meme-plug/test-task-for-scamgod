from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.client.bot import DefaultBotProperties

from services.news_fetcher import NewsFetcher
from services.api_fetcher import APIFetcher
from bot.handlers.commands import router as commands_router
from bot.handlers.callbacks import router as callbacks_router

class TGBot:
    def __init__(self, BOT_API_TOKEN: str, api_fetcher: APIFetcher):
        self.bot = Bot(token=BOT_API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
        self.dp = Dispatcher(storage=MemoryStorage())
        self.api_fetcher = api_fetcher
        self.news_fetcher = NewsFetcher(self.api_fetcher, self.bot)
        
    def _setup_handlers(self):
        self.dp.include_router(commands_router)
        self.dp.include_router(callbacks_router)
        
    async def start(self):
        self._setup_handlers()
        await self._set_bot_commands()
        await self.news_fetcher.start()
        await self.dp.start_polling(self.bot)

    async def stop(self):
        await self.news_fetcher.stop()
        await self.bot.session.close()

    async def _set_bot_commands(self):
        await self.bot.set_my_commands([
            BotCommand(command="/start", description="Начать работу с ботом")
        ])