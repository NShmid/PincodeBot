import asyncio
import os
from dotenv import find_dotenv, load_dotenv

from aiogram import Bot
from aiogram import Dispatcher, types
from aiogram.fsm.strategy import FSMStrategy

from core.handlers.user_handler import user_router
from core.handlers.product_feed import product_feed_router


load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

dp.include_router(product_feed_router)
dp.include_router(user_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands([types.BotCommand(command='start', description='Запустить бота')])
    await dp.start_polling(bot)
    

asyncio.run(main())