from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == "subscription_manager")
async def subscription_manager_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Менеджер подписок",
        reply_markup=get_subscription_manager_menu()
    )
    await callback.answer()