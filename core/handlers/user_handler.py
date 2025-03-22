from aiogram import Router, types
from aiogram.filters import Command

from core.keyboards.reply_keyboards import user_menu

user_router = Router()


@user_router.message(Command("start"))
async def user_start(message: types.Message):
    await message.answer("Привет! Выбери что тебе нужно", reply_markup=user_menu)
    

@user_router.message()
async def user_start(message: types.Message):
    await message.answer(message.text)