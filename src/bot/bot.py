from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from services.news_fetcher import NewsFetcher
from services.api_fetcher import APIFetcher
from bot.handlers import commands, callbacks

class TGBot:
    def __init__(self, BOT_API_TOKEN: str):
        self.bot = Bot(token=BOT_API_TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.api_fetcher = APIFetcher()
        self.news_fetcher = NewsFetcher(self.api_fetcher, self.bot)
        
    def _setup_handlers(self):
        self.dp.include_router(commands.router)
        self.dp.include_router(callbacks.router)
        
    async def start(self):
        await self._set_bot_commands()
        await self.news_fetcher.start()
        await self.dp.start_polling(self.bot)

    async def _set_bot_commands(self):
        await self.bot.set_my_commands([
            BotCommand(command="/start", description="Начать работу с ботом")
        ])