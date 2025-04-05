from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from core.keyboards.reply_keyboards import user_main_menu, seller_main_menu, orders_menu
from core.keyboards.inline_keyboards import get_user_order_keyboard
from core.database import db
from core.utils.main_state import MainState
from core.filters.emoji_filter import TextNormalizer

from datetime import datetime


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
@user_router.message(StateFilter("*"), F.text.func(TextNormalizer("главное меню")))
async def back_to_main_menu(message: types.Message, state: FSMContext):
    keyboard = seller_main_menu if message.from_user.id in db.sellers else user_main_menu
    await message.answer("Возвращаю в главное меню...", reply_markup=keyboard)
    await state.set_state(MainState.view_main)


@user_router.message(F.text.func(TextNormalizer("инструкция")))
async def user_instruction(message: types.Message):
    await message.answer("Инструкция")


# Функция для отображения одного заказа
async def show_order_item(message: types.Message, bot: Bot, current_index: int, state: FSMContext, 
                           mode="create"):
    data = await state.get_data()
    orders = data.get("orders")
    if not orders:
        await message.answer("У вас нет активных заказов.")
        return
    
    order = orders[current_index]
    order_id = order[0]
    order_descr = order[1]
    delivery_date = datetime.strptime(order[4], "%Y-%m-%d %H:%M:%S")
    delivery_time = order[5]
    order_status = order[6]
    
    text = (f"Заказ №<b>{order_id}</b>\n\n"
            f"🛒 <b>Содержимое:</b>\n"
            f"{order_descr}\n\n"
            f"🕒 <b>Дата и время доставки:</b> {delivery_date.strftime('%d.%m.%Y')} {delivery_time}\n\n"
            f"<b>🔸 Статус заказа: {order_status}</b>\n\n"
            f"Заказ {current_index + 1} из {len(orders)}"
        )
    
    # Сохраняем текущий индекс в состоянии
    await state.update_data(current_index=current_index)
    
    if mode == "create":
        msg = await message.answer(
            text=text, 
            parse_mode="HTML",
            reply_markup=get_user_order_keyboard(current_index, len(orders))
        )
        await state.update_data(last_order_msg_id=msg.message_id)
    elif mode == "move":
        await bot.edit_message_text(
            text=text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=get_user_order_keyboard(current_index, len(orders)),
            parse_mode="HTML"
        )


# Функция для отображения заказов пользователя
@user_router.message(MainState.view_main, F.text.func(TextNormalizer("мои заказы")))
async def get_user_orders(message: types.Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    orders = db.get_orders(user_id)
    
    await state.set_state(MainState.view_orders)
    
    data = await state.get_data()
    last_order_msg_id = data.get("last_order_msg_id")
    if last_order_msg_id:
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=last_order_msg_id,
            reply_markup=None
        )
        await state.update_data(last_basket_msg_id=None)
    
    await state.update_data(orders=orders)
    await state.update_data(current_index=0)
    await message.answer("Загружаю заказы...", reply_markup=orders_menu)
    await show_order_item(message, bot, 0, state, mode="create")


# Функция для инлайн кнопок в заказах пользователя
@user_router.callback_query(MainState.view_orders)
async def redo_undo_orders(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    current_index = data.get("current_index")
    orders = data.get("orders")
    
    choice = callback.data
    if "Далее" in choice:
        if current_index < len(orders) - 1:
            current_index += 1
            await show_order_item(callback.message, bot, current_index, state, mode="move")
            
    elif "Назад" in choice:
        if current_index > 0:
            current_index -= 1
            await show_order_item(callback.message, bot, current_index, state, mode="move")
    
    await callback.answer()  # Закрываем callback
    

@user_router.message()
async def user_start(message: types.Message):
    await message.answer("Выбери что-нибудь из меню")