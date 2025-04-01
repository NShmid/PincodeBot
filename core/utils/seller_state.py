from aiogram.fsm.state import State, StatesGroup


class SellerState(StatesGroup):
    view_seller_main = State()
    view_orders = State()
    
    # Добавление товара
    set_name_product = State()
    set_caption_product = State()
    set_image_product = State()
    set_count_product = State()
    set_price_product = State()