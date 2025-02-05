from src.core.database.models import User

async def is_admin(user_id: int) -> bool:
    user = await User.get(id=user_id)
    return user.is_admin