"""
Сервис выдачи уроков по расписанию.
Читает content_assets/course_*/schedule.json и отправляет уроки пользователям.
"""
import json
import logging
from pathlib import Path
from datetime import datetime

from database import get_active_users_for_lessons, was_lesson_sent, mark_lesson_sent

# Путь к content_assets относительно корня проекта (родитель course_bot)
CONTENT_ROOT = Path(__file__).resolve().parent.parent.parent / "content_assets"
DEFAULT_COURSE = "course_tazovoe_dno"


def load_schedule(course_slug=DEFAULT_COURSE):
    """Загрузить расписание курса из schedule.json"""
    path = CONTENT_ROOT / course_slug / "schedule.json"
    if not path.exists():
        logging.warning(f"Schedule not found: {path}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_lessons_for_day(schedule, day):
    """Получить уроки для дня N курса"""
    if not schedule or "lessons" not in schedule:
        return []
    return [l for l in schedule["lessons"] if l.get("day") == day]


def compute_course_day(payment_date_str):
    """
    Вычислить день курса (1-based).
    payment_date — дата оплаты в формате YYYY-MM-DD.
    """
    try:
        payment = datetime.strptime(payment_date_str[:10], "%Y-%m-%d")
        today = datetime.now().date()
        delta = (today - payment.date()).days
        return max(1, delta + 1)  # День 1 = день оплаты
    except (ValueError, TypeError):
        return 1


async def send_lessons(bot):
    """
    Разослать уроки всем активным пользователям по расписанию.
    Вызывается из scheduler раз в день.
    """
    schedule = load_schedule()
    if not schedule:
        return

    users = await get_active_users_for_lessons()
    sent_count = 0

    for tg_id, payment_date in users:
        day = compute_course_day(payment_date)
        lessons = get_lessons_for_day(schedule, day)

        for lesson in lessons:
            lesson_id = lesson.get("lesson_id", "")
            if not lesson_id:
                continue

            if await was_lesson_sent(tg_id, lesson_id):
                continue

            title = lesson.get("title", "Урок")
            url = lesson.get("url", "")
            description = lesson.get("description", "")

            text = f"📚 **Урок {day}. {title}**\n\n"
            if description:
                text += f"{description}\n\n"
            if url:
                text += f"▶️ Смотреть: {url}\n\n"
            text += "Сдать ДЗ: /hw"

            try:
                await bot.send_message(tg_id, text, parse_mode="Markdown")
                await mark_lesson_sent(tg_id, lesson_id)
                sent_count += 1
                logging.info(f"Lesson {lesson_id} sent to {tg_id}")
            except Exception as e:
                logging.error(f"Failed to send lesson to {tg_id}: {e}")

    if sent_count:
        logging.info(f"Lessons sent: {sent_count}")
