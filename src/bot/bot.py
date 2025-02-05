from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

class TGBot:
    def __init__(self, BOT_API_TOKEN: str):
        self.bot = Bot(token=BOT_API_TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())
        
    def _setup_handlers(self):
        self.dp.include_routers()
        
    async def start(self):
        await self.dp.start_polling(self.bot)