from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime

from bot.buttons.menu import get_main_menu
from core.database.models import User

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    user, created = await User.get_or_create(
        id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        }
    )
    
    user.last_active = datetime.now()
    await user.save()
    
    await message.answer(
        "Выберите действие:",
        reply_markup=get_main_menu()
    )