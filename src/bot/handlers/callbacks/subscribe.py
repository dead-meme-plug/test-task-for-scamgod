from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from bot.buttons.menu import get_subscription_manager_menu, get_main_menu
from core.database.models import User, Subscription
from utils.states import SubscriptionStates

router = Router()

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
    subscriptions = await Subscription.filter(user=user)
    
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
    await state.set_state(SubscriptionStates.waiting_for_topic)
    await callback.answer()

@router.message(StateFilter(SubscriptionStates.waiting_for_topic))
async def process_topic_handler(message: Message, state: FSMContext):
    topic = message.text.strip()

    user, created = await User.get_or_create(
        id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        }
    )
    
    if await Subscription.filter(user=user, topic=topic).exists():
        await message.answer(
            f"Вы уже подписаны на тему '{topic}'.",
            reply_markup=get_subscription_manager_menu()
        )
    else:
        await Subscription.create(user=user, topic=topic)
        await message.answer(
            f"Вы успешно подписались на тему '{topic}'!",
            reply_markup=get_subscription_manager_menu()
        )
    
    await state.clear()

@router.callback_query(F.data == "remove_subscription")
async def remove_subscription_handler(callback: CallbackQuery):
    user = await User.get(id=callback.from_user.id)
    subscriptions = await Subscription.filter(user=user)
    
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
    
    await Subscription.filter(user=user, topic=topic).delete()
    await callback.message.edit_text(
        f"Вы отписались от темы '{topic}'.",
        reply_markup=get_subscription_manager_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "main_menu")
async def back_to_main_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите действие:",
        reply_markup=get_main_menu()
    )
    await callback.answer()