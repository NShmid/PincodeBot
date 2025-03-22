from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_main_menu = ReplyKeyboardMarkup(
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

product_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Еще товары"),
            KeyboardButton(text="Корзина")
        ],
        [
            KeyboardButton(text="Главное меню"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

basket_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главное меню"),
            KeyboardButton(text="Оформить заказ")
        ],
        [
            KeyboardButton(text="Лента товаров")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)