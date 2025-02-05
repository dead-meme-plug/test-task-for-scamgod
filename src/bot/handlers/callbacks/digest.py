from aiogram import Router
from aiogram.types import CallbackQuery
from src.bot.buttons.menu import get_digest_menu

router = Router()

@router.callback_query(lambda c: c.data == "get_digest")
async def get_digest_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Ваш дайджест:",
        reply_markup=get_digest_menu()
    )
    await callback.answer()