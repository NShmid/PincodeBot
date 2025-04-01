from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import secrets

from core.keyboards.reply_keyboards import user_main_menu
from core.database.db import admins, add_token


admin_router = Router()


@admin_router.message(Command("link"))
async def user_start(message: types.Message, bot: Bot, state: FSMContext):
    if message.from_user.id in admins:
        await state.clear()
        
        bot_username = (await bot.get_me()).username
        token = secrets.token_urlsafe(16)
        start_link = f"https://t.me/{bot_username}?start={token}"
        
        add_token(message.from_user.id, token)
        
        await message.answer(
            f"Индивидуальная ссылка-приглашение:\n{start_link}",
            reply_markup=None
        )