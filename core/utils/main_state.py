from aiogram.fsm.state import State, StatesGroup


offset = {}

class MainState(StatesGroup):
    view_main = State()
    view_products = State()
    view_basket = State()
    choose_time_delivery = State()
    confirm_delivery = State()