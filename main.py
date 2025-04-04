import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from aiogram_calendar import SimpleCalendarCallback

from aiogram import Bot
from aiogram import Dispatcher, types
from aiogram.fsm.strategy import FSMStrategy

from core.handlers.user_handler import user_router
from core.handlers.product_feed import product_feed_router
from core.handlers.basket import basket_router, get_date_delivery
from core.handlers.admin_handler import admin_router
from core.handlers.seller_handler import seller_router
from core.database.db import create_tables
from core.utils.set_commands import set_commands


load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

dp.include_routers(product_feed_router, basket_router, admin_router, seller_router, user_router)
dp.callback_query.register(get_date_delivery, SimpleCalendarCallback.filter())

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    create_tables()
    await set_commands(bot)
    await dp.start_polling(bot)
    

asyncio.run(main())