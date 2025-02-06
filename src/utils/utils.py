from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from datetime import datetime

from core.database.models import User

async def is_admin(user_id: int) -> bool:
    user = await User.get(id=user_id)
    return user.is_admin

class BanCheck(BaseMiddleware):
    
    async def __call__(self, handler, event: types.Message | types.CallbackQuery, data: dict):
        if isinstance(event, types.Message):
            user = event.from_user
        elif isinstance(event, types.CallbackQuery):
            user = event.from_user
        else:
            return await handler(event, data)

        user = await User.get(id=user.id)
        if user.is_banned and (user.ban_expires_at is None or user.ban_expires_at > datetime.now()):
            await event.answer(f"Вы заблокированы в боте до {str(user.ban_expires_at)}")
            return
        return await handler(event, data)

class UserCreationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message | types.CallbackQuery, data: dict):
        if isinstance(event, types.Message):
            user = event.from_user
        elif isinstance(event, types.CallbackQuery):
            user = event.from_user
        else:
            return await handler(event, data)

        user_id = user.id
        await User.get_or_create(
            id=user_id,
            defaults={
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
        return await handler(event, data)