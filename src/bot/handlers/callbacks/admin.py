from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime, timedelta

from bot.buttons.menu import get_admin_menu, get_user_management_menu, get_main_menu
from core.database.models import User
from utils.states import AdminStates
from utils.utils import is_admin

router = Router()

@router.callback_query(F.data == "admin_statistics")
async def admin_statistics_handler(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой команде.")
        return

    total_users = await User.all().count()
    active_users = await User.filter(is_active=True).count()
    banned_users = await User.filter(is_banned=True).count()
    
    await callback.message.edit_text(
        f"Статистика:\n\n"
        f"Всего пользователей: {total_users}\n"
        f"Активных пользователей: {active_users}\n"
        f"Забаненных пользователей: {banned_users}",
        reply_markup=get_admin_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_users")
async def admin_users_handler(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой команде.")
        return

    await callback.message.edit_text(
        "Управление пользователями",
        reply_markup=get_user_management_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_ban_user")
async def admin_ban_user_handler(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой команде.")
        return

    await callback.message.edit_text(
        "Введите ID пользователя и срок бана (например, '12345 1d'):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="admin_users")]
        ])
    )
    await state.set_state(AdminStates.waiting_for_ban_details)
    await callback.answer()

@router.message(StateFilter(AdminStates.waiting_for_ban_details))
async def process_ban_details_handler(message: Message, state: FSMContext):
    try:
        user_id, ban_duration = message.text.split()
        user_id = int(user_id)
        ban_duration = parse_ban_duration(ban_duration)
        
        user = await User.get(id=user_id)
        if not user:
            await message.answer("Пользователь не найден.")
            return

        user.is_banned = True
        user.ban_expires_at = datetime.now() + ban_duration
        await user.save()

        await message.answer(
            f"Пользователь {user_id} забанен до {user.ban_expires_at}.",
            reply_markup=get_admin_menu()
        )
    except Exception as e:
        await message.answer(
            "Неверный формат. Пример: '12345 1d'.",
            reply_markup=get_admin_menu()
        )
    finally:
        await state.clear()

@router.callback_query(F.data == "admin_toggle_admin")
async def admin_toggle_admin_handler(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой команде.")
        return

    await callback.message.edit_text(
        "Введите ID пользователя:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="admin_users")]
        ])
    )
    await state.set_state(AdminStates.waiting_for_user_id)
    await callback.answer()

@router.message(StateFilter(AdminStates.waiting_for_user_id))
async def process_user_id_handler(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        user = await User.get(id=user_id)
        if not user:
            await message.answer("Пользователь не найден.")
            return

        user.is_admin = not user.is_admin
        await user.save()

        await message.answer(
            f"Пользователь {user_id} {'теперь админ' if user.is_admin else 'больше не админ'}.",
            reply_markup=get_admin_menu()
        )
    except ValueError:
        await message.answer(
            "Неверный формат. Введите ID пользователя.",
            reply_markup=get_admin_menu()
        )
    finally:
        await state.clear()

@router.callback_query(F.data == "main_menu")
async def back_to_main_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите действие:",
        reply_markup=get_main_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_panel")
async def back_to_admin_panel_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Админская панель",
        reply_markup=get_admin_menu()
    )
    await callback.answer()

def parse_ban_duration(duration: str) -> timedelta:
    if duration.endswith("m"):
        return timedelta(minutes=int(duration[:-1]))
    elif duration.endswith("h"):
        return timedelta(hours=int(duration[:-1]))
    elif duration.endswith("d"):
        return timedelta(days=int(duration[:-1]))
    elif duration.endswith("M"):
        return timedelta(days=int(duration[:-1]) * 30)
    elif duration.endswith("y"):
        return timedelta(days=int(duration[:-1]) * 365)
    else:
        raise ValueError("Неверный формат срока бана.")