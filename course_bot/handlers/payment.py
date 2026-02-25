import logging
import re
import hmac
import hashlib
from datetime import datetime, timedelta
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ChatJoinRequest
from aiogram.fsm.context import FSMContext
from config import PRODAMUS_SECRET_KEY, COURSE_DURATION_DAYS, CHANNEL_ID, CHAT_ID, ADMIN_IDS
from database import add_user, get_user, add_payment, get_payment
from services.sheets import add_user_to_sheet
from keyboards import main_menu

router = Router()

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def calculate_access_date(days=COURSE_DURATION_DAYS):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")


def verify_prodamus_signature(data: dict, secret_key: str) -> bool:
    """Проверка HMAC-подписи от Prodamus"""
    received_sign = data.pop('sign', None)
    if not received_sign or not secret_key:
        return False

    # Сортируем параметры и собираем строку
    sorted_params = sorted(data.items())
    sign_string = '&'.join(f'{k}={v}' for k, v in sorted_params)
    expected_sign = hmac.new(
        secret_key.encode(), sign_string.encode(), hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_sign, received_sign)


# --- Вебхук от Prodamus ---

async def handle_prodamus_webhook(data: dict, bot: Bot) -> bool:
    """
    Обработчик webhook от Prodamus. Вызывается из bot.py через aiohttp.
    data: dict с полями от Продамуса (order_id, sum, customer_email, sign и т.д.)
    """
    try:
        # 1. Проверка подписи
        data_copy = dict(data)
        if PRODAMUS_SECRET_KEY and not verify_prodamus_signature(data_copy, PRODAMUS_SECRET_KEY):
            logging.warning("Invalid Prodamus webhook signature")
            return False

        # 2. Получение данных
        email = data.get('customer_email')
        phone = data.get('customer_phone', 'unknown')
        amount = data.get('sum', '0')

        if not email:
            logging.error("No email in webhook data")
            return False

        logging.info(f"Payment received from {email}, sum: {amount}")

        # 3. Сохраняем оплату в БД
        await add_payment(email, amount)

        # 4. Записываем в Google Sheet (без tg_id — пользователь ещё не активировался)
        try:
            sheet_data = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'tg_id': "WAITING",
                'username': "",
                'email': email,
                'phone': phone,
                'amount': amount,
                'end_date': calculate_access_date()
            }
            add_user_to_sheet(sheet_data)
        except Exception as e:
            logging.error(f"Sheet error: {e}")

        return True
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return False


# --- Команды бота ---

@router.message(Command("start"))
async def cmd_start(message: Message):
    args = message.text.split()

    if len(args) > 1 and args[1] == 'pay':
        await message.answer(
            "🎉 Спасибо за оплату!\n\n"
            "Чтобы получить доступ, введи email, который указывал при покупке:\n"
            "/activate твой@email.com"
        )
    else:
        await message.answer(
            "Привет! Я бот курса.\n"
            "Если ты уже оплатил участие, используй email, который указывал при покупке, "
            "чтобы активировать доступ.\n\n"
            "Введи команду: /activate твой@email.com"
        )


@router.message(Command("activate"))
async def cmd_activate(message: Message):
    try:
        email = message.text.split()[1]

        # Валидация email
        if not EMAIL_REGEX.match(email):
            await message.answer("❌ Некорректный email. Проверь формат: имя@домен.зона")
            return

        # Проверка оплаты
        payment = await get_payment(email)
        if not payment:
            await message.answer(
                "❌ Оплата с этим email не найдена.\n\n"
                "Убедись, что указал тот же email, что и при оплате. "
                "Если только что оплатил — подожди пару минут и попробуй снова."
            )
            return

        # Добавляем пользователя
        end_date = calculate_access_date()
        payment_date = datetime.now().strftime("%Y-%m-%d")
        await add_user(
            tg_id=message.from_user.id,
            username=message.from_user.username or "",
            full_name=message.from_user.full_name or "User",
            email=email,
            phone="unknown",
            payment_date=payment_date,
            access_end_date=end_date
        )

        # Приветственное сообщение
        channel_link = await message.bot.create_chat_invite_link(CHANNEL_ID, member_limit=1)
        chat_link = await message.bot.create_chat_invite_link(CHAT_ID, member_limit=1)
        welcome_text = (
            f"✅ Оплата найдена! Доступ открыт до {end_date}.\n\n"
            "📌 **Как устроен курс:**\n"
            "• Уроки приходят в бота по расписанию (раз в день)\n"
            "• Домашние задания сдаёшь командой /hw — присылай видео\n"
            "• Вопросы задавай в чате курса\n\n"
            f"1️⃣ Канал с материалами: {channel_link.invite_link}\n"
            f"2️⃣ Чат участников: {chat_link.invite_link}\n\n"
            "Жду тебя внутри! 🧘‍♀️"
        )
        await message.answer(welcome_text, reply_markup=main_menu, parse_mode="Markdown")

        # Пишем в Google Sheet
        try:
            sheet_data = {
                'date': payment_date,
                'tg_id': message.from_user.id,
                'username': message.from_user.username or "",
                'email': email,
                'phone': "unknown",
                'amount': "manual",
                'end_date': end_date
            }
            add_user_to_sheet(sheet_data)
        except Exception as e:
            logging.error(f"Sheet error: {e}")

    except IndexError:
        await message.answer("Использование: /activate ваш@email.com")


# --- КОМАНДА ДЛЯ ТЕСТА (только для админов) ---
@router.message(Command("test_pay"))
async def cmd_test_pay(message: Message):
    """Выдает доступ без оплаты (только для админов)"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Эта команда доступна только администраторам.")
        return

    try:
        end_date = calculate_access_date()
        await add_user(
            tg_id=message.from_user.id,
            username=message.from_user.username or "",
            full_name=message.from_user.full_name or "User",
            email="test@admin.com",
            phone="79990000000",
            payment_date=datetime.now().strftime("%Y-%m-%d"),
            access_end_date=end_date
        )
        await message.answer(
            f"🕵️ РЕЖИМ ТЕСТИРОВАНИЯ\n\n"
            f"Вам выдан доступ до {end_date}.\n"
            f"Теперь работают кнопки ниже.",
            reply_markup=main_menu
        )
    except Exception as e:
        logging.error(f"test_pay error: {e}")
        await message.answer(f"Ошибка: {e}. Попробуй /menu")


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Показать меню с кнопками"""
    await message.answer("Выбери действие:", reply_markup=main_menu)


@router.message(F.text == "🆘 Помощь")
async def cmd_help(message: Message, state: FSMContext):
    """Обработка кнопки Помощь"""
    await state.clear()
    await message.answer(
        "📌 **Помощь по боту:**\n\n"
        "• **Сдать ДЗ** — пришли видео с выполненным заданием\n"
        "• **Оставить отзыв** — напиши или пришли фото с отзывом о курсе\n"
        "• **Мой профиль** — информация о твоём доступе\n\n"
        "Если возникли вопросы — напиши куратору в чат курса.",
        parse_mode="Markdown"
    )


# --- Мой профиль ---
@router.message(F.text == "👤 Мой профиль")
async def cmd_profile(message: Message, state: FSMContext):
    """Обработка кнопки «Мой профиль»"""
    await state.clear()
    user = await get_user(message.from_user.id)

    if not user:
        await message.answer("Ты пока не зарегистрирован. Используй /activate для активации.")
        return

    # user: (id, tg_id, username, full_name, email, phone, payment_date, access_end_date, is_active)
    full_name = user[3] or "—"
    email = user[4] or "—"
    payment_date = user[6] or "—"
    access_end = user[7] or "—"
    is_active = user[8]

    status = "✅ Активен" if is_active else "❌ Не активен"

    text = (
        f"👤 **Мой профиль**\n\n"
        f"Имя: {full_name}\n"
        f"Email: {email}\n"
        f"Дата оплаты: {payment_date}\n"
        f"Доступ до: {access_end}\n"
        f"Статус: {status}"
    )
    await message.answer(text, parse_mode="Markdown")


# --- Обработка заявок на вступление (Approve Join Request) ---
@router.chat_join_request()
async def approve_request(update: ChatJoinRequest, bot: Bot):
    user = await get_user(update.from_user.id)
    # user: (id, tg_id, username, full_name, email, phone, payment_date, access_end_date, is_active)
    is_active = user[8] if user and len(user) > 8 else False
    if user and is_active:
        await update.approve()
        await bot.send_message(update.from_user.id, "Заявка одобрена! Добро пожаловать.")
    else:
        await update.decline()
        await bot.send_message(update.from_user.id, "Доступ запрещен. Оплатите курс на сайте.")
