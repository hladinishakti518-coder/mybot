import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from pytz import timezone
from database import get_users_expiring_in, get_expired_users, deactivate_user
from config import CHANNEL_ID, NOTIFICATION_DAYS_BEFORE
from services.lessons import send_lessons

logging.basicConfig(level=logging.INFO)

MSK = timezone('Europe/Moscow')


class AccessScheduler:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone=MSK)
        # Уроки — каждый день в 09:00 МСК
        self.scheduler.add_job(self.deliver_lessons, 'cron', hour=9, minute=0)
        # Проверка доступов — каждый день в 10:00 МСК
        self.scheduler.add_job(self.check_access, 'cron', hour=10, minute=0)

    async def start(self):
        self.scheduler.start()
        logging.info("Scheduler started (timezone: Europe/Moscow).")

    async def deliver_lessons(self):
        """Рассылка уроков по расписанию"""
        try:
            await send_lessons(self.bot)
        except Exception as e:
            logging.error(f"Lesson delivery error: {e}")

    async def check_access(self):
        """Ежедневная проверка доступов"""
        logging.info("Checking user access rights...")

        # 1. Отправка напоминаний (за 30, 14, 3 дня)
        for days_left in NOTIFICATION_DAYS_BEFORE:
            try:
                expiring_users = await get_users_expiring_in(days_left)
                for user_id, full_name in expiring_users:
                    try:
                        await self.bot.send_message(
                            user_id,
                            f"🔔 {full_name}, твой доступ к курсу заканчивается через {days_left} дней! "
                            "Поторопись сдать долги по ДЗ."
                        )
                    except Exception as e:
                        logging.warning(f"Could not notify user {user_id}: {e}")
            except Exception as e:
                logging.error(f"Error checking expiring users: {e}")

        # 2. Удаление просроченных
        try:
            expired_users = await get_expired_users()
            for (user_id,) in expired_users:
                try:
                    await self.bot.send_message(
                        user_id,
                        "🚫 Твой доступ к материалам курса завершен.\n"
                        "Ты остаешься в чате выпускников, но из канала я тебя удаляю."
                    )
                    await self.bot.ban_chat_member(CHANNEL_ID, user_id)
                    await deactivate_user(user_id)
                    logging.info(f"User {user_id} removed from channel.")
                except Exception as e:
                    logging.error(f"Failed to kick user {user_id}: {e}")
        except Exception as e:
            logging.error(f"Error processing expired users: {e}")
