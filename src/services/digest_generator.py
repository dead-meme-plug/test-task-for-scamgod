from datetime import datetime, timedelta
from typing import List, Dict, Any
from core.database.models import User, Article, Subscription
from services.text_analyzer import TextAnalyzer

class DigestGenerator:
    
    def __init__(self, text_analyzer: TextAnalyzer):
        self.text_analyzer = text_analyzer

    async def generate_digest(self, user_id: int, days: int = 7) -> Dict[str, Any]:
        user = await User.get(id=user_id)
        subscriptions = await Subscription.filter(user=user, is_active=True).values_list("topic", flat=True)
        
        if not subscriptions:
            return {"message": "У вас нет активных подписок"}

        articles = await self._get_recent_articles_by_topics(subscriptions, days)
        
        if not articles:
            return {"message": "Нет новых статей по вашим подпискам"}

        grouped_articles = self._group_articles_by_topic(articles, subscriptions)
        analyzed_articles = await self._analyze_articles(articles)

        return {
            "user_id": user_id,
            "period_days": days,
            "total_articles": len(articles),
            "grouped_articles": grouped_articles,
            "analyzed_articles": analyzed_articles
        }

    async def _get_recent_articles_by_topics(self, topics: List[str], days: int) -> List[Article]:
        date_threshold = datetime.now() - timedelta(days=days)
        articles = await Article.filter(created_at__gte=date_threshold).all()

        topics_lower = [topic.lower() for topic in topics]
        
        filtered_articles = [
            article for article in articles
            if any(topic.lower() in article.title.lower() for topic in topics_lower)
        ]
        
        return sorted(filtered_articles, key=lambda x: x.published_at, reverse=True)

    def _group_articles_by_topic(self, articles: List[Article], topics: List[str]) -> Dict[str, List[Dict]]:
        grouped = {topic: [] for topic in topics}
        for article in articles:
            for topic in topics:
                if topic.lower() in article.title.lower():
                    grouped[topic].append({
                        "title": article.title,
                        "source": article.source,
                        "url": article.url,
                        "published_at": article.published_at.strftime("%Y-%m-%d %H:%M")
                    })
        return grouped

    async def _analyze_articles(self, articles: List[Article]) -> Dict[str, Any]:
        if not articles:
            return {}

        all_text = " ".join(article.title + " " + (article.content or "") for article in articles)
        keywords = self.text_analyzer.extract_keywords(all_text, top_n=10)
        sentiment = self.text_analyzer.analyze_sentiment(all_text)

        return {
            "keywords": keywords,
            "sentiment": sentiment
        }