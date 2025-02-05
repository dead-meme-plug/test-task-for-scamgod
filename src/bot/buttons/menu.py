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

def get_subscription_manager_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Мои подписки", callback_data="my_subscriptions")
        ],
        [
            InlineKeyboardButton(text="Добавить подписку", callback_data="add_subscription")
        ],
        [
            InlineKeyboardButton(text="Удалить подписку", callback_data="remove_subscription")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="main_menu")
        ]
    ])

def get_digest_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Получить дайджест за неделю", callback_data="digest_week")
        ],
        [
            InlineKeyboardButton(text="Получить дайджест за месяц", callback_data="digest_month")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="main_menu")
        ]
    ])