from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from src.bot.buttons.menu import get_subscription_manager_menu
from src.core.database.models import User
from src.services.subscription_service import SubscriptionService

router = Router()
subscription_service = SubscriptionService()

@router.callback_query(F.data == "subscription_manager")
async def subscription_manager_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Менеджер подписок",
        reply_markup=get_subscription_manager_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "my_subscriptions")
async def my_subscriptions_handler(callback: CallbackQuery):
    user = await User.get(id=callback.from_user.id)
    subscriptions = await subscription_service.get_user_subscriptions(user)
    
    if not subscriptions:
        await callback.message.edit_text(
            "У вас пока нет активных подписок.",
            reply_markup=get_subscription_manager_menu()
        )
    else:
        await callback.message.edit_text(
            f"Ваши активные подписки:\n\n• " + "\n• ".join([sub.topic for sub in subscriptions]),
            reply_markup=get_subscription_manager_menu()
        )
    await callback.answer()

@router.callback_query(F.data == "add_subscription")
async def add_subscription_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Введите тему для новой подписки:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="subscription_manager")]
        ])
    )
    await state.set_state("waiting_for_topic")
    await callback.answer()

@router.message(StateFilter("waiting_for_topic"))
async def process_topic_handler(message: Message, state: FSMContext):
    topic = message.text.strip()
    user = await User.get(id=message.from_user.id)
    
    if await subscription_service.get_user_subscriptions(user):
        await message.answer(
            f"Вы уже подписаны на тему '{topic}'.",
            reply_markup=get_subscription_manager_menu()
        )
    else:
        await subscription_service.add_subscription(user, topic)
        await message.answer(
            f"Вы успешно подписались на тему '{topic}'!",
            reply_markup=get_subscription_manager_menu()
        )
    
    await state.clear()

@router.callback_query(F.data == "remove_subscription")
async def remove_subscription_handler(callback: CallbackQuery):
    user = await User.get(id=callback.from_user.id)
    subscriptions = await subscription_service.get_user_subscriptions(user)
    
    if not subscriptions:
        await callback.message.edit_text(
            "У вас пока нет активных подписок.",
            reply_markup=get_subscription_manager_menu()
        )
    else:
        await callback.message.edit_text(
            "Выберите подписку для удаления:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=sub.topic, callback_data=f"remove_subscription_{sub.topic}")]
                for sub in subscriptions
            ] + [
                [InlineKeyboardButton(text="Назад", callback_data="subscription_manager")]
            ])
        )
    await callback.answer()

@router.callback_query(F.data.startswith("remove_subscription_"))
async def process_remove_subscription_handler(callback: CallbackQuery):
    topic = callback.data.replace("remove_subscription_", "")
    user = await User.get(id=callback.from_user.id)
    
    await subscription_service.remove_subscription(user, topic)
    await callback.message.edit_text(
        f"Вы отписались от темы '{topic}'.",
        reply_markup=get_subscription_manager_menu()
    )
    await callback.answer()