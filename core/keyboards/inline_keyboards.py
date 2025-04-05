from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_user_product_feed_keyboard(product_id):
    product_feed_keyboard = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_to_basket_{product_id}")],
            [InlineKeyboardButton(text="Предзаказ", callback_data=f"preorder_{product_id}")]
        ]
    )
    
    return product_feed_keyboard


def get_admin_product_feed_keyboard(product_id):
    product_feed_keyboard = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Удалить товар", callback_data=f"delete_{product_id}")],
            [InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_to_basket_{product_id}")],
            [InlineKeyboardButton(text="Предзаказ", callback_data=f"preorder_{product_id}")]
        ]
    )
    
    return product_feed_keyboard


def get_basket_keyboard(current_index, len_basket, product_id):
    keyboard = []
    
    if len_basket == 1:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="-1", callback_data=f"-1_{product_id}"),
                    InlineKeyboardButton(text="+1", callback_data=f"+1_{product_id}")
                ],
                [
                    InlineKeyboardButton(text="Удалить товар ❌", callback_data=f"Удалить_{product_id}"),
                ]
            ]
        )
    elif current_index == 0 and len_basket > 1:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="-1", callback_data=f"-1_{product_id}"),
                    InlineKeyboardButton(text="+1", callback_data=f"+1_{product_id}")
                ],
                                [
                    InlineKeyboardButton(text="Удалить товар ❌", callback_data=f"Удалить_{product_id}"),
                ],
                [
                    InlineKeyboardButton(text="Далее ➡️", callback_data=f"Далее_{product_id}")
                ],
            ]
        )
    elif current_index > 0 and current_index < len_basket - 1:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="-1", callback_data=f"-1_{product_id}"),
                    InlineKeyboardButton(text="+1", callback_data=f"+1_{product_id}")
                ],
                                [
                    InlineKeyboardButton(text="Удалить товар ❌", callback_data=f"Удалить_{product_id}"),
                ],
                [
                    InlineKeyboardButton(text="Назад ⬅️", callback_data=f"Назад_{product_id}"),
                    InlineKeyboardButton(text="Далее ➡️", callback_data=f"Далее_{product_id}")
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="-1", callback_data=f"-1_{product_id}"),
                    InlineKeyboardButton(text="+1", callback_data=f"+1_{product_id}")
                ],
                [
                    InlineKeyboardButton(text="Удалить товар ❌", callback_data=f"Удалить_{product_id}"),
                ],
                [
                    InlineKeyboardButton(text="Назад ⬅️", callback_data=f"Назад_{product_id}"),
                ],
            ]
        )
    
    return keyboard


def get_user_order_keyboard(current_index: int, len_orders: int):
    if len_orders == 1:
        return None
    
    keyboard = []
    if current_index == 0 and len_orders > 1:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Далее ➡️", callback_data=f"Далее")
                ],
            ]
        )
    elif current_index > 0 and current_index < len_orders - 1:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Назад ⬅️", callback_data=f"Назад"),
                    InlineKeyboardButton(text="Далее ➡️", callback_data=f"Далее")
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Назад ⬅️", callback_data=f"Назад"),
                ],
            ]
        )
    
    return keyboard


def get_delivery_time_kb():
    delivery_time_keyboard = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="с 10 до 13", callback_data=f"с 10 до 13"),
                InlineKeyboardButton(text="с 15 до 18", callback_data=f"с 15 до 18")
            ]
        ]
    )
    
    return delivery_time_keyboard