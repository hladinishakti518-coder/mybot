import logging
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_IDS, CURATORS_CHAT_ID

router = Router()

class FeedbackState(StatesGroup):
    waiting_for_review = State()

# --- Вход в режим "Отзыва" ---
@router.message(F.text == "⭐️ Оставить отзыв")
async def cmd_feedback_start(message: Message, state: FSMContext):
    await message.answer(
        "📝 **Напиши свой отзыв о курсе!**\n\n"
        "Это может быть текст, фото, видео или голосовое сообщение.\n"
        "Мы ценим любую обратную связь!",
        parse_mode="Markdown"
    )
    await state.set_state(FeedbackState.waiting_for_review)

# --- Прием самого отзыва ---
@router.message(FeedbackState.waiting_for_review)
async def process_feedback(message: Message, state: FSMContext, bot: Bot):
    user = message.from_user
    
    # Получаем текст отзыва (если он есть в сообщении или подписи)
    review_text = message.text or message.caption or ""
    
    # Заголовок для админа
    header = (
        f"⭐️ **Новый отзыв!**\n"
        f"👤 От: {user.full_name} (@{user.username})\n"
        f"🆔 ID: {user.id}\n\n"
    )
    
    # Полный текст сообщения
    full_text = f"{header}{review_text}"
    
    # Обрезаем, если слишком длинно для caption (1024 символа)
    if len(full_text) > 1024:
        full_text = full_text[:1020] + "..."

    try:
        # Отправляем админам
        for admin_id in ADMIN_IDS:
            if message.text:
                 # Если просто текст - отправляем как обычное сообщение
                 await bot.send_message(chat_id=admin_id, text=full_text)
            else:
                 # Если фото/видео/голос - копируем сообщение и добавляем нашу подпись
                 await message.copy_to(chat_id=admin_id, caption=full_text)

        await message.answer("✅ Спасибо за отзыв! Нам очень приятно.")
    except Exception as e:
        logging.error(f"Failed to forward feedback: {e}")
        await message.answer("Произошла ошибка при отправке. Попробуй позже.")
    
    # Сбрасываем состояние (возвращаем в обычный режим)
    await state.clear()
