import asyncio
import logging
import os
import hmac
import hashlib
from aiohttp import web

# Переходим в папку бота, чтобы .env и БД находились корректно
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH, PRODAMUS_SECRET_KEY
from database import init_db
from handlers import payment, homework, admin, feedback
from services.scheduler import AccessScheduler
from aiogram.fsm.storage.memory import MemoryStorage

WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8080"))


async def handle_prodamus_webhook(request):
    """Обработчик POST-запросов от Prodamus"""
    try:
        data = await request.json()
    except Exception:
        data = dict(await request.post())

    bot = request.app["bot"]
    result = await payment.handle_prodamus_webhook(data, bot)

    if result:
        return web.Response(text="OK", status=200)
    else:
        return web.Response(text="Error", status=400)


async def on_startup(bot: Bot):
    logging.info("Starting bot...")
    await init_db()

    # Запуск планировщика
    scheduler = AccessScheduler(bot)
    await scheduler.start()

    logging.info("Bot started successfully!")


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем роутеры
    dp.include_router(payment.router)
    dp.include_router(homework.router)
    dp.include_router(admin.router)
    dp.include_router(feedback.router)

    await on_startup(bot)

    # Создаём aiohttp-приложение для приёма вебхуков от Prodamus
    app = web.Application()
    app["bot"] = bot
    app.router.add_post(WEBHOOK_PATH, handle_prodamus_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", WEBHOOK_PORT)
    await site.start()
    logging.info(f"Prodamus webhook server listening on port {WEBHOOK_PORT}, path {WEBHOOK_PATH}")

    # Запускаем polling параллельно с aiohttp-сервером
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
