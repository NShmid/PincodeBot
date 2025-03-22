from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_product_feed_keyboard(product_id):
    product_feed_keyboard = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_to_basket_{product_id}")],
            [InlineKeyboardButton(text="Предзаказ", callback_data=f"preorder_{product_id}")]
        ]
    )
    
    return product_feed_keyboard


def get_basket_keyboard(current_index, len_basket, product_id):
    keyboard = []
    
    if current_index == 0:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="-1", callback_data=f"-1_{product_id}"),
                    InlineKeyboardButton(text="+1", callback_data=f"-1_{product_id}")
                ],
                [
                    InlineKeyboardButton(text="Далее", callback_data=f"Далее_{product_id}")
                ]
            ]
        )
    elif current_index > 0 and current_index < len_basket - 1:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="-1", callback_data=f"-1_{product_id}"),
                    InlineKeyboardButton(text="+1", callback_data=f"-1_{product_id}")
                ],
                [
                    InlineKeyboardButton(text="Назад", callback_data=f"Назад_{product_id}"),
                    InlineKeyboardButton(text="Далее", callback_data=f"Далее_{product_id}")
                ]
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="-1", callback_data=f"-1_{product_id}"),
                    InlineKeyboardButton(text="+1", callback_data=f"-1_{product_id}")
                ],
                [
                    InlineKeyboardButton(text="Назад", callback_data=f"Назад_{product_id}"),
                ]
            ]
        )
    
    return keyboard