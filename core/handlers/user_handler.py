from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.keyboards.reply_keyboards import user_main_menu
from core.database import db


user_router = Router()


@user_router.message(Command("start"))
async def user_start(message: types.Message):
    db.create_tables()
    await message.answer("Привет! Выбери что тебе нужно", reply_markup=user_main_menu)
     
    
@user_router.message()
async def user_start(message: types.Message):
    await message.answer("Выбери что-нибудь из меню")