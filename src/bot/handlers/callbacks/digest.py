from aiogram import Router, F
from aiogram.types import CallbackQuery
from typing import Dict, Any

from bot.buttons.menu import get_digest_menu, get_main_menu
from core.database.models import User
from services.digest_generator import DigestGenerator
from services.text_analyzer import TextAnalyzer

router = Router()
text_analyzer = TextAnalyzer()
digest_generator = DigestGenerator(text_analyzer)

@router.callback_query(lambda c: c.data == "get_digest")
async def get_digest_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Ваш дайджест:",
        reply_markup=get_digest_menu()
    )
    await callback.answer()
    
@router.callback_query(F.data == "get_digest")
async def get_digest_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите период для дайджеста:",
        reply_markup=get_digest_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "digest_week")
async def digest_week_handler(callback: CallbackQuery):
    user = await User.get(id=callback.from_user.id)
    digest = await digest_generator.generate_digest(user.id, days=7)
    
    if "message" in digest:
        await callback.message.edit_text(
            digest["message"],
            reply_markup=get_main_menu()
        )
    else:
        await callback.message.edit_text(
            f"Ваш дайджест за неделю:\n\n{_format_digest(digest)}",
            reply_markup=get_main_menu()
        )
    await callback.answer()

@router.callback_query(F.data == "digest_month")
async def digest_month_handler(callback: CallbackQuery):
    user = await User.get(id=callback.from_user.id)
    digest = await digest_generator.generate_digest(user.id, days=30)
    
    if "message" in digest:
        await callback.message.edit_text(
            digest["message"],
            reply_markup=get_main_menu()
        )
    else:
        await callback.message.edit_text(
            f"Ваш дайджест за месяц:\n\n{_format_digest(digest)}",
            reply_markup=get_main_menu()
        )
    await callback.answer()
    
@router.callback_query(F.data == "main_menu")
async def back_to_main_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите действие:",
        reply_markup=get_main_menu()
    )
    await callback.answer()

def _format_digest(digest: Dict[str, Any]) -> str:
    result = []
    
    for topic, articles in digest["grouped_articles"].items():
        result.append(f"📌 <b>{topic}</b>:")
        for article in articles:
            title = article['title']
            url = article['url']
            result.append(f"• <a href='{url}'>{title}</a>")
        result.append("")

    analysis = digest.get("analyzed_articles", {})
    if analysis:
        keywords = analysis.get("keywords", [])
        if isinstance(keywords, str):
            keywords = keywords.split(", ")  
        result.append(f"<b>Ключевые слова</b>: {', '.join(keywords[:5])}")
        sentiment = analysis.get('sentiment', 0.0)
        result.append(f"<b>Сентиментальность</b>: {sentiment:.2f}")
    
    return "\n".join(result)