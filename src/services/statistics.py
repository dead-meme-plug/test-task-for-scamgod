from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Any, List
from core.database.models import User, Subscription, Article
from tortoise.functions import Count
class IStatisticsService(ABC):
    
    @abstractmethod
    async def get_basic_stats(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_user_activity_stats(self, days: int = 7) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_subscription_stats(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_article_stats(self) -> Dict[str, Any]:
        pass

class StatisticsService(IStatisticsService):

    async def get_basic_stats(self) -> Dict[str, Any]:
        return {
            "total_users": await User.all().count(),
            "active_users": await self._get_active_users_count(),
            "total_subscriptions": await Subscription.all().count(),
            "total_articles": await Article.all().count(),
        }

    async def get_user_activity_stats(self, days: int = 7) -> Dict[str, Any]:
        active_threshold = datetime.now() - timedelta(days=days)
        return {
            "active_users_last_week": await User.filter(
                last_active__gte=active_threshold
            ).count(),
            "new_users_last_week": await User.filter(
                created_at__gte=active_threshold
            ).count(),
        }

    async def get_subscription_stats(self) -> Dict[str, Any]:
        return {
            "total_subscriptions": await Subscription.all().count(),
            "active_subscriptions": await Subscription.filter(
                is_active=True
            ).count(),
            "most_popular_topics": await self._get_most_popular_topics(),
        }

    async def get_article_stats(self) -> Dict[str, Any]:
        return {
            "total_articles": await Article.all().count(),
            "articles_last_week": await Article.filter(
                created_at__gte=datetime.now() - timedelta(days=7)
            ).count(),
            "most_active_sources": await self._get_most_active_sources(),
        }

    async def _get_active_users_count(self) -> int:
        active_threshold = datetime.now() - timedelta(days=30)
        return await User.filter(last_active__gte=active_threshold).count()

    async def _get_most_popular_topics(self, limit: int = 5) -> List[Dict[str, Any]]:
        return (
            await Subscription.annotate(count=Count("topic"))
            .group_by("topic")
            .order_by("-count")
            .limit(limit)
            .values("topic", "count")
        )

    async def _get_most_active_sources(self, limit: int = 5) -> List[Dict[str, Any]]:
        return (
            await Article.annotate(count=Count("source"))
            .group_by("source")
            .order_by("-count")
            .limit(limit)
            .values("source", "count")
        )