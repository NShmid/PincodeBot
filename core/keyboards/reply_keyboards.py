from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Инструкция 📄"),
            KeyboardButton(text="Лента товаров 🛍️")
        ],
        [
            KeyboardButton(text="Корзина 🛒"),
            KeyboardButton(text="Мои заказы 📋")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

seller_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Инструкция 📄"),
            KeyboardButton(text="Лента товаров 🛍️")
        ],
        [
            KeyboardButton(text="Корзина 🛒"),
            KeyboardButton(text="Мои заказы 📋"),
        ],
        [
            KeyboardButton(text="Панель продавца ⚙️"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

product_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Еще товары 🛍️"),
            KeyboardButton(text="Корзина 🛒")
        ],
        [
            KeyboardButton(text="Главное меню 🎛️"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

basket_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главное меню 🎛️"),
            KeyboardButton(text="Оформить заказ ✔️")
        ],
        [
            KeyboardButton(text="Лента товаров 🛍️"),
            KeyboardButton(text="Очистить корзину 🧹")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

seller_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Заявки 📝"),
            KeyboardButton(text="Добавить товар ➕")
        ],
        [
            KeyboardButton(text="Главное меню 🎛️"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

orders_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главное меню 🎛️"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

add_product_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главное меню 🎛️"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

cancel_delivery = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена ❌"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

confirm_delivery = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подтвердить ✔️"),
            KeyboardButton(text="Отмена ❌"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)