import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из папки course_bot (где лежит config.py)
load_dotenv(Path(__file__).parent / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id_str) for id_str in os.getenv("ADMIN_IDS", "").split(",") if id_str]
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ID канала с материалами
CHAT_ID = os.getenv("CHAT_ID")        # ID чата болталки
CURATORS_CHAT_ID = os.getenv("CURATORS_CHAT_ID") # ID чата для проверки ДЗ

PRODAMUS_SECRET_KEY = os.getenv("PRODAMUS_SECRET_KEY")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")

# Настройки курса
COURSE_DURATION_DAYS = int(os.getenv("COURSE_DURATION_DAYS", "90"))
NOTIFICATION_DAYS_BEFORE = [int(x) for x in os.getenv("NOTIFICATION_DAYS_BEFORE", "30,14,3").split(",") if x.strip()]
