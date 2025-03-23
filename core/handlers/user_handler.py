from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from core.keyboards.reply_keyboards import user_main_menu
from core.database import db
from core.utils.main_state import MainState


user_router = Router()


@user_router.message(Command("start"))
async def user_start(message: types.Message, state: FSMContext):
    db.create_tables()
    await state.set_state(MainState.view_main)
    await message.answer("Привет! Выбери что тебе нужно", reply_markup=user_main_menu)
     

# Функция для возврата в главное меню
@user_router.message(StateFilter("*"), F.text.lower() == "главное меню")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await message.answer("Возвращаю в главное меню...", reply_markup=user_main_menu)
    await state.set_state(MainState.view_main)


@user_router.message()
async def user_start(message: types.Message):
    await message.answer("Выбери что-нибудь из меню")