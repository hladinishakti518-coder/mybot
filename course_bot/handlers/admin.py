import asyncio
import logging
from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_IDS
from database import get_all_active_users

router = Router()

@router.message(Command("broadcast", "bc"))
async def cmd_broadcast(message: Message, bot: Bot):
    """
    Команда для рассылки сообщения всем активным пользователям.
    Использование: /bc Текст сообщения
    """
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔️ Эта команда доступна только администраторам.")
        return

    # Получаем текст рассылки (все, что после команды /bc)
    text = message.text.split(maxsplit=1)
    if len(text) < 2:
        await message.answer("⚠️ Ошибка: Введи текст рассылки.\nПример: `/bc Завтра вебинар в 19:00!`", parse_mode="Markdown")
        return
    
    broadcast_text = text[1]
    
    # Получаем список получателей
    users = await get_all_active_users()
    if not users:
        await message.answer("ℹ️ В базе нет активных пользователей для рассылки.")
        return

    await message.answer(f"🚀 Начинаю рассылку для {len(users)} пользователей...")

    success_count = 0
    fail_count = 0

    for user_id in users:
        try:
            await bot.send_message(user_id, broadcast_text)
            success_count += 1
            # Пауза, чтобы не словить спам-блок от Telegram (30 сообщений в секунду)
            await asyncio.sleep(0.05) 
        except Exception as e:
            logging.error(f"Failed to send to {user_id}: {e}")
            fail_count += 1

    await message.answer(
        f"✅ **Рассылка завершена!**\n\n"
        f"📤 Успешно: {success_count}\n"
        f"❌ Ошибок: {fail_count} (обычно это те, кто заблокировал бота)",
        parse_mode="Markdown"
    )
