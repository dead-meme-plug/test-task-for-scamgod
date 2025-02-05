from tortoise import fields, models
from datetime import datetime

class User(models.Model):
    id = fields.BigIntField(pk=True) #именно телеграм айдишка
    username = fields.CharField(max_length=32, null=True)
    first_name = fields.CharField(max_length=64)
    last_name = fields.CharField(max_length=64, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_active = fields.DatetimeField(auto_now=True)
    is_admin = fields.BooleanField(default=False)
    
    subscriptions: fields.ReverseRelation["Subscription"]
    received_articles: fields.ManyToManyRelation["Article"]
    class Meta:
        table = "users"
        
class Subscription(models.Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="subscriptions"
    )
    topic = fields.CharField(max_length=128)  # Тема/ключевое слово
    created_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)
    class Meta:
        table = "subscriptions"
        unique_together = (("user", "topic"),)
        
class Article(models.Model):
    id = fields.UUIDField(pk=True)
    source = fields.CharField(max_length=128)
    title = fields.TextField()
    description = fields.TextField(null=True)
    url = fields.CharField(max_length=512, unique=True)
    url_to_image = fields.CharField(max_length=512, null=True)
    published_at = fields.DatetimeField()
    content = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    users: fields.ManyToManyRelation[User] = fields.ManyToManyField(
        "models.User", related_name="received_articles", through="user_articles"
    )
    analysis: fields.ReverseRelation["ArticleAnalysis"]

    class Meta:
        table = "articles"
        
class ArticleAnalysis(models.Model):
    id = fields.IntField(pk=True)
    article: fields.OneToOneRelation[Article] = fields.OneToOneField(
        "models.Article", related_name="analysis"
    )
    keywords = fields.JSONField()  # ключевые слова
    sentiment_score = fields.FloatField(null=True)  # сентиментальность
    word_frequencies = fields.JSONField()  # частота слов
    created_at = fields.DatetimeField(auto_now_add=True)
    class Meta:
        table = "article_analyses"
        

class BotState(models.Model):
    key = fields.CharField(max_length=255, uniqie=True)
    value = fields.TextField()
    
    class Meta:
        table = "bot_state"