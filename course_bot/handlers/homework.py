import logging
from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import CURATORS_CHAT_ID
from database import add_homework, get_user
from services.lessons import compute_course_day

_CURATORS_CHAT_ID = int(CURATORS_CHAT_ID) if CURATORS_CHAT_ID else None

router = Router()


class HomeworkState(StatesGroup):
    waiting_for_video = State()


@router.message(Command("hw"))
async def cmd_homework(message: Message, state: FSMContext):
    """Команда для сдачи ДЗ"""
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Сначала оплати курс! /start")
        return

    # Определяем текущий день курса по дате оплаты
    payment_date = user[6]
    course_day = compute_course_day(payment_date)

    await state.set_state(HomeworkState.waiting_for_video)
    await state.update_data(lesson_number=course_day)

    await message.answer(
        f"📚 Сдача ДЗ за урок {course_day}.\n\n"
        "Пришли мне видео с выполненным заданием.\n"
        "Я перешлю его куратору."
    )


@router.message(HomeworkState.waiting_for_video, F.video | F.video_note | F.document)
async def handle_video_hw(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id

    user = await get_user(user_id)
    if not user:
        await message.answer("Сначала оплати курс! /start")
        return

    # Получаем номер урока из FSM
    data = await state.get_data()
    lesson_number = data.get("lesson_number", 1)

    # Сохраняем в БД
    file_id = message.video.file_id if message.video else (
        message.video_note.file_id if message.video_note else message.document.file_id
    )

    hw_id = await add_homework(user_id, file_id, lesson_number=lesson_number)

    # Отправляем кураторам
    try:
        caption = (
            f"📚 Новое ДЗ!\n"
            f"👤 Ученик: {message.from_user.full_name} (@{message.from_user.username})\n"
            f"🆔 ID: {user_id}\n"
            f"📝 Урок: {lesson_number}\n"
            f"#hw_{hw_id}"
        )

        if message.video:
            await bot.send_video(chat_id=_CURATORS_CHAT_ID, video=file_id, caption=caption)
        elif message.video_note:
            await bot.send_video_note(chat_id=_CURATORS_CHAT_ID, video_note=file_id)
            await bot.send_message(chat_id=_CURATORS_CHAT_ID, text=caption)
        else:
            await bot.send_document(chat_id=_CURATORS_CHAT_ID, document=file_id, caption=caption)

        await message.answer("✅ ДЗ отправлено куратору! Жди ответа.")

    except Exception as e:
        logging.error(f"Failed to send HW to curators: {e}")
        await message.answer("Ошибка при отправке. Попробуй позже.")

    await state.clear()


@router.message(HomeworkState.waiting_for_video)
async def handle_invalid_hw(message: Message):
    """Если прислали не видео/документ в режиме ДЗ"""
    await message.answer("Пришли видео или документ с выполненным заданием.")


# --- Ответ куратора (Reply) ---
@router.message(F.reply_to_message, F.chat.id == _CURATORS_CHAT_ID)
async def handle_curator_reply(message: Message, bot: Bot):
    """
    Куратор отвечает на сообщение с ДЗ в чате кураторов.
    Бот пересылает ответ ученику.
    """
    try:
        original_caption = message.reply_to_message.caption or message.reply_to_message.text

        if not original_caption or "ID:" not in original_caption:
            return

        # Парсим ID (ищем строку "ID: 12345")
        user_id_line = [line for line in original_caption.split('\n') if "ID:" in line][0]
        student_id = int(user_id_line.split(":")[1].strip())

        await bot.send_message(
            chat_id=student_id,
            text=f"🧑‍🏫 **Ответ куратора:**\n\n{message.text}",
            parse_mode="Markdown"
        )

        await message.reply("✅ Ответ отправлен ученику.")

    except Exception as e:
        logging.error(f"Error handling curator reply: {e}")
        await message.reply(f"Ошибка доставки ответа: {e}")
