from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from core.keyboards.reply_keyboards import user_main_menu, seller_main_menu
from core.database import db
from core.utils.main_state import MainState


user_router = Router()


@user_router.message(Command("start"))
async def user_start(message: types.Message, state: FSMContext):
    args = message.text.split(" ", 1)
    
    if len(args) > 1:
        if not db.is_new_seller(message.from_user.id):
            await message.answer(
                "Вы не можете использовать эту ссылку",
                reply_markup=user_main_menu
            )
            return
            
        token = args[1]
        if not db.is_token_used(token):
            db.activate_token(message.from_user.id, token)
            db.sellers = db.get_sellers()
            await message.answer(
                "Привет, продавец! Ссылка активирована",
                reply_markup=seller_main_menu
            )
        else:
            await message.answer("Это ссылка недействительна", reply_markup=user_main_menu)
    else:
        if message.from_user.id in db.sellers:
            await message.answer("Привет, продавец!", reply_markup=seller_main_menu)
        else:
            await message.answer("Привет, покупатель!", reply_markup=user_main_menu)
    
    await state.set_state(MainState.view_main)
     

# Функция для возврата в главное меню
@user_router.message(StateFilter("*"), F.text.lower() == "главное меню")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    keyboard = seller_main_menu if message.from_user.id in db.sellers else user_main_menu
    await message.answer("Возвращаю в главное меню...", reply_markup=keyboard)
    await state.set_state(MainState.view_main)


@user_router.message(F.text.lower() == "инструкция")
async def user_instruction(message: types.Message):
    await message.answer("Инструкция")


@user_router.message()
async def user_start(message: types.Message):
    await message.answer("Выбери что-нибудь из меню")