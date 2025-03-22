from aiogram.fsm.state import State, StatesGroup


offset = {}

class MainState(StatesGroup):
    view_products = State()
    view_basket = State()