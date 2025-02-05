from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from src.bot.handlers import commands, callbacks

class TGBot:
    def __init__(self, BOT_API_TOKEN: str):
        self.bot = Bot(token=BOT_API_TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())
        
    def _setup_handlers(self):
        self.dp.include_router(commands.router)
        self.dp.include_router(callbacks.router)
        
    async def start(self):
        await self._set_bot_commands()
        await self.dp.start_polling(self.bot)

    async def _set_bot_commands(self):
        await self.bot.set_my_commands([
            BotCommand(command="/start", description="Начать работу с ботом")
        ])