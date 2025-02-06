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

def get_admin_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Статистика", callback_data="admin_statistics")
        ],
        [
            InlineKeyboardButton(text="Пользователи", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="main_menu")
        ]
    ])

def get_user_management_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Забанить пользователя", callback_data="admin_ban_user")
        ],
        [
            InlineKeyboardButton(text="Выдать/отнять админку", callback_data="admin_toggle_admin")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="admin_panel")
        ]
    ])