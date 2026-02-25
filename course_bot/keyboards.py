from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Сдать ДЗ"), KeyboardButton(text="👤 Мой профиль")],
        [KeyboardButton(text="⭐️ Оставить отзыв"), KeyboardButton(text="🆘 Помощь")]
    ],
    resize_keyboard=True,
    is_persistent=True
)
