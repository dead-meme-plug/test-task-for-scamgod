from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.buttons.menu import get_admin_menu
from utils.utils import is_admin

router = Router()

@router.message(Command("admin"))
async def admin_command_handler(message: Message):
    if not await is_admin(message.from_user.id):
        await message.answer("У вас нет доступа к этой команде.")
        return

    await message.answer(
        "Админская панель",
        reply_markup=get_admin_menu()
    )