from core.database.models import Subscription, User
from typing import List

class SubscriptionService:
    async def add_subscription(self, user: User, topic: str) -> Subscription:
        return await Subscription.create(user=user, topic=topic)

    async def remove_subscription(self, user: User, topic: str) -> None:
        await Subscription.filter(user=user, topic=topic).update(is_active=False)

    async def get_user_subscriptions(self, user: User) -> List[Subscription]:
        return await Subscription.filter(user=user, is_active=True)