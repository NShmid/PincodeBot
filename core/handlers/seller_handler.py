from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from core.keyboards.reply_keyboards import seller_panel, orders_menu, add_product_menu
from core.database import db
from core.utils.main_state import MainState
from core.utils.seller_state import SellerState
from core.filters.seller_filter import IsSeller


seller_router = Router()


# Функция для перехода в панель продавца
@seller_router.message(IsSeller(), MainState.view_main, F.text.lower() == "панель продавца")
async def get_panel_seller(message: types.Message, state: FSMContext):
    await message.answer("Вы перешли в панель продавца", reply_markup=seller_panel)
    await state.set_state(SellerState.view_seller_main)
    

# Функция для просмотра заявок
@seller_router.message(SellerState.view_seller_main, F.text.lower() == "заявки")
async def get_orders(message: types.Message, state: FSMContext):
    await message.answer("Вы выбрали заявки", reply_markup=orders_menu)
    await state.set_state(SellerState.view_orders)
    

# Функция для просмотра заявок
@seller_router.message(SellerState.view_seller_main, F.text.lower() == "добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Вы выбрали добавить товар", reply_markup=add_product_menu)
    await state.set_state(SellerState.set_name_product)