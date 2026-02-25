import os
import aiosqlite
from datetime import datetime, timedelta

DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "course_bot.db")

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE,
                username TEXT,
                full_name TEXT,
                email TEXT,
                phone TEXT,
                payment_date TEXT,
                access_end_date TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS homeworks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                lesson_number INTEGER,
                file_id TEXT,
                status TEXT DEFAULT 'pending', -- pending, approved, rejected
                submitted_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(tg_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lesson_progress (
                user_id INTEGER,
                lesson_id TEXT,
                sent_at TEXT,
                PRIMARY KEY (user_id, lesson_id),
                FOREIGN KEY (user_id) REFERENCES users(tg_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                amount TEXT,
                paid_at TEXT
            )
        """)
        await db.commit()

async def add_user(tg_id, username, full_name, email, phone, payment_date, access_end_date):
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute("""
                INSERT INTO users (tg_id, username, full_name, email, phone, payment_date, access_end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (tg_id, username, full_name, email, phone, payment_date, access_end_date))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            # Пользователь уже существует, обновляем подписку
            await db.execute("""
                UPDATE users 
                SET access_end_date = ?, is_active = 1
                WHERE tg_id = ?
            """, (access_end_date, tg_id))
            await db.commit()
            return False

async def get_user(tg_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,)) as cursor:
            return await cursor.fetchone()

async def get_users_expiring_in(days: int):
    """Найти пользователей, у которых доступ истекает через N дней"""
    target_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    # Ищем по точной дате (или диапазону, если нужно)
    # Здесь упрощенно: ищем тех, у кого дата окончания совпадает с сегодняшней + days
    # В реальном проекте лучше проверять диапазон
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT tg_id, full_name FROM users WHERE access_end_date LIKE ? AND is_active = 1", 
            (f"{target_date}%",)
        ) as cursor:
            return await cursor.fetchall()

async def get_expired_users():
    """Найти пользователей, у которых доступ истек вчера/сегодня"""
    now = datetime.now().strftime("%Y-%m-%d")
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT tg_id FROM users WHERE access_end_date < ? AND is_active = 1", 
            (now,)
        ) as cursor:
            return await cursor.fetchall()

async def deactivate_user(tg_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET is_active = 0 WHERE tg_id = ?", (tg_id,))
        await db.commit()

async def get_all_active_users():
    """Получить ID всех активных пользователей для рассылки"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT tg_id FROM users WHERE is_active = 1") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def get_active_users_for_lessons():
    """Получить (tg_id, payment_date) активных пользователей для рассылки уроков"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT tg_id, payment_date FROM users WHERE is_active = 1 AND payment_date IS NOT NULL"
        ) as cursor:
            rows = await cursor.fetchall()
            return [(row[0], row[1]) for row in rows]

# --- Работа с оплатами ---
async def add_payment(email: str, amount: str):
    paid_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO payments (email, amount, paid_at) VALUES (?, ?, ?)",
            (email.lower(), amount, paid_at)
        )
        await db.commit()

async def get_payment(email: str):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT email, amount, paid_at FROM payments WHERE email = ?",
            (email.lower(),)
        ) as cursor:
            return await cursor.fetchone()


# --- Работа с уроками ---
async def was_lesson_sent(user_id, lesson_id):
    """Проверить, отправлялся ли урок пользователю"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT 1 FROM lesson_progress WHERE user_id = ? AND lesson_id = ?",
            (user_id, lesson_id)
        ) as cursor:
            return (await cursor.fetchone()) is not None

async def mark_lesson_sent(user_id, lesson_id):
    """Отметить урок как отправленный"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO lesson_progress (user_id, lesson_id, sent_at) VALUES (?, ?, ?)",
            (user_id, lesson_id, now)
        )
        await db.commit()

# --- Работа с ДЗ ---
async def add_homework(user_id, file_id, lesson_number=1):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "INSERT INTO homeworks (user_id, lesson_number, file_id, submitted_at) VALUES (?, ?, ?, ?)",
            (user_id, lesson_number, file_id, now)
        )
        await db.commit()
        return cursor.lastrowid
