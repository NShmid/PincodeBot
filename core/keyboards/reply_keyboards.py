from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Инструкция"),
            KeyboardButton(text="Лента товаров")
        ],
        [
            KeyboardButton(text="Корзина")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)