from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from core.keyboards.reply_keyboards import seller_panel, orders_menu, add_product_menu
from core.keyboards.inline_keyboards import get_seller_order_keyboard
from core.database import db
from core.utils.main_state import MainState
from core.utils.seller_state import SellerState
from core.filters.seller_filter import IsSeller
from core.filters.emoji_filter import TextNormalizer

from datetime import datetime
import secrets


seller_router = Router()


# Функция для перехода в панель продавца
@seller_router.message(IsSeller(), MainState.view_main, F.text.func(TextNormalizer("панель продавца")))
async def get_panel_seller(message: types.Message, state: FSMContext):
    await message.answer("Вы перешли в панель продавца", reply_markup=seller_panel)
    await state.set_state(SellerState.view_seller_main)
        

# Функция для отображения одного заказа
async def show_sel_order_item(message: types.Message, bot: Bot, current_index: int, state: FSMContext, 
                           mode="create"):
    data = await state.get_data()
    orders = data.get("all_orders")
    if not orders:
        await message.answer("У вас нет активных заказов.")
        return
    
    order = orders[current_index]
    order_id = order[0]
    order_descr = order[1]
    user_id = order[2]
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
    await state.update_data(current_index=current_index, order_id=order_id, user_id=user_id)
    
    if mode == "create":
        msg = await message.answer(
            text=text, 
            parse_mode="HTML",
            reply_markup=get_seller_order_keyboard(current_index, len(orders), order_id)
        )
        await state.update_data(last_order_sel_msg_id=msg.message_id)
    elif mode in ["move", "delete"]:
        await bot.edit_message_text(
            text=text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=get_seller_order_keyboard(current_index, len(orders), order_id),
            parse_mode="HTML"
        )    
    

# Функция для просмотра заявок
@seller_router.message(SellerState.view_seller_main, F.text.func(TextNormalizer("заявки")))
async def get_orders(message: types.Message, bot: Bot, state: FSMContext):
    all_orders = db.get_all_active_orders()
    
    await state.set_state(SellerState.view_orders)
    
    data = await state.get_data()
    last_order_sel_msg_id = data.get("last_order_sel_msg_id")
    if last_order_sel_msg_id:
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=last_order_sel_msg_id,
            reply_markup=None
        )
        await state.update_data(last_order_sel_msg_id=None)
    
    await state.update_data(all_orders=all_orders)
    await state.update_data(current_index=0)
    await message.answer("Загружаю заявки...", reply_markup=orders_menu)
    await show_sel_order_item(message, bot, 0, state, mode="create")


# Функция для инлайн кнопок в заказах пользователя
@seller_router.callback_query(SellerState.view_orders)
async def redo_undo_orders(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    current_index = data.get("current_index")
    all_orders = data.get("all_orders")
    order_id = data.get("order_id")
    user_id = data.get("user_id")
    
    choice = callback.data
    if "Далее" in choice:
        if current_index < len(all_orders) - 1:
            current_index += 1
            await show_sel_order_item(callback.message, bot, current_index, state, mode="move")
            
    elif "Назад" in choice:
        if current_index > 0:
            current_index -= 1
            await show_sel_order_item(callback.message, bot, current_index, state, mode="move")
    
    elif "Принять" in choice:
        pincode = ''.join(secrets.choice('0123456789') for _ in range(4))
        db.approve_order(order_id, pincode)
        all_orders.pop(current_index)
        if current_index == len(all_orders):
            current_index -= 1
        
        await state.update_data(all_orders=all_orders, current_index=current_index)
        if len(all_orders) == 0:
            data = await state.get_data()
            last_order_msg = data.get("last_order_sel_msg_id")
            await bot.edit_message_reply_markup(
                chat_id=callback.message.chat.id,
                message_id=last_order_msg,
                reply_markup=None
            )
        await show_sel_order_item(callback.message, bot, current_index, state, mode="delete")
        
        await callback.answer("Заявка одобрена")
        await bot.send_message(
            chat_id=user_id,
            text=f"Ваш закакз №{order_id} одобрен! ПИН-код для камеры смотрите в информации к заказу."
        )
    
    elif "Отклонить" in choice:
        db.reject_order(order_id)
        all_orders.pop(current_index)
        if current_index == len(all_orders):
            current_index -= 1
        
        await state.update_data(all_orders=all_orders, current_index=current_index)
        if len(all_orders) == 0:
            data = await state.get_data()
            last_order_msg = data.get("last_order_sel_msg_id")
            await bot.edit_message_reply_markup(
                chat_id=callback.message.chat.id,
                message_id=last_order_msg,
                reply_markup=None
            )
        await show_sel_order_item(callback.message, bot, current_index, state, mode="delete")
        
        await callback.answer("Заявка отклонена")
        await bot.send_message(
            chat_id=user_id,
            text=f"Ваш закакз №{order_id} отклонен!."
        )
        
    await callback.answer()  # Закрываем callback