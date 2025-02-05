from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Менеджер подписок", callback_data="subscription_manager")
        ],
        [
            InlineKeyboardButton(text="Получить дайджест", callback_data="get_digest")
        ]
    ])