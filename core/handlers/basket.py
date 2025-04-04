from core.database import db
from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.filters.callback_data import CallbackData

from core.keyboards.reply_keyboards import user_main_menu, basket_menu, seller_main_menu
from core.keyboards.inline_keyboards import get_basket_keyboard, get_delivery_time_kb
from core.keyboards.reply_keyboards import product_menu, cancel_delivery, confirm_delivery
from core.database import db
from core.utils.main_state import MainState
from core.filters.emoji_filter import TextNormalizer

import aiogram_calendar as ac
from datetime import datetime, timedelta


basket_router = Router()


# Функция для отображения одного товара из корзины
async def show_basket_item(message: types.Message, bot: Bot, current_index: int, state: FSMContext, 
                           mode="create"):
    data = await state.get_data()
    basket = data.get("basket")
    if not basket:
        await message.answer("Корзина пуста")
        return
    
    ### Первое сообщение ###
    product_id, count = basket[current_index]
    product = db.get_product(product_id)[0]
    product_name = product[1]
    product_descr = product[2]
    product_count = product[3]
    product_price = product[4]
    product_image = types.FSInputFile(f"images/{product_id}.jpg")
    
    caption = (f"<b>{product_name}</b>\n"
    f"Описание: {product_descr}\n"
    f"Количество: {product_count}\n"
    f"Цена: {product_price}\n\n"
    f"Товар {current_index + 1} из {len(basket)}")
    
    # Сохраняем текущий индекс в состоянии
    await state.update_data(current_index=current_index)
    
    if mode == "create":
        msg = await message.answer_photo(photo=product_image, caption=caption, parse_mode="HTML",
                         reply_markup=get_basket_keyboard(current_index, len(basket), product_id))
        await state.update_data(last_basket_msg_id=msg.message_id)
    elif mode in ("move", "delete"):
        file = types.InputMediaPhoto(media=product_image, caption=caption, parse_mode="HTML")
        await bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.message_id,
            media=file,
            reply_markup=get_basket_keyboard(current_index, len(basket), product_id)
        )
    
    answer = "<b>Содержимое корзины:</b>\n"
    
    ### Второе сообщение ###    
    price = 0
    for x in basket:
        product_id = x[0]
        count = x[1]
        
        product = db.get_product(product_id)[0]
        product_name = product[1]
        product_price = product[-1]
        
        answer += f"{product_name} - {count} шт.\n"
        price += round(count * product_price, 2)
    
    answer += f"\nОбщая стоимость: {price} рублей"
    
    if mode == "create":
        m = await message.answer(answer, parse_mode="HTML")
        a = m.message_id if len(basket) > 1 else None
        await state.update_data(last_basket_msg=a)
    elif mode in ("+-1", "delete"):
        data = await state.get_data()
        last_basket_msg = data.get("last_basket_msg")
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_basket_msg,
            text=answer,
            parse_mode="HTML"
        )


# Функция для просмотра корзины из ленты или из главного меню
@basket_router.message(StateFilter(MainState.view_products, MainState.view_main),
                       F.text.func(TextNormalizer('корзина')))
async def get_basket(message: types.Message, bot: Bot, state: FSMContext):   
    user_id = message.from_user.id
    basket = db.get_basket(user_id)
    
    await state.set_state(MainState.view_basket)
    
    data = await state.get_data()
    last_basket_msg_id = data.get("last_basket_msg_id")
    if last_basket_msg_id:
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=last_basket_msg_id,
            reply_markup=None
        )
        await state.update_data(last_basket_msg_id=None)
    
    await state.update_data(basket=basket)
    await state.update_data(current_index=0)
    await message.answer("Загружаю корзину...", reply_markup=basket_menu)
    await show_basket_item(message, bot, 0, state, mode="create")
    

# Функция для инлайн кнопок в корзине
@basket_router.callback_query(MainState.view_basket)
async def redo_undo_basket(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    current_index = data.get("current_index")
    basket = data.get("basket")
    product_id, count = basket[current_index]
    user_id = callback.from_user.id
    
    choice = callback.data
    if "Далее_" in choice:
        if current_index < len(basket) - 1:
            current_index += 1
            await show_basket_item(callback.message, bot, current_index, state, mode="move")
        
        await callback.answer()  # Закрываем callback
    elif "Назад_" in choice:
        if current_index > 0:
            current_index -= 1
            await show_basket_item(callback.message, bot, current_index, state, mode="move")
    
        await callback.answer()  # Закрываем callback
    elif "+1_" in choice:
        product_count = db.get_product(product_id)[0][-2]
        if count <= product_count:
            db.adding_one(user_id, product_id)
            basket[current_index] = basket[current_index][0], basket[current_index][-1] + 1
            await state.update_data(basket=basket)
            await show_basket_item(callback.message, bot, current_index, state, mode="+-1")
            await callback.answer("Количество товара изменено")
        else:
            await callback.answer("Вы не можете больше добавить этот товар")
        
    elif "-1_" in choice:
        if count > 1:
            db.subtraction_one(user_id, product_id)
            basket[current_index] = basket[current_index][0], basket[current_index][-1] - 1
            await state.update_data(basket=basket, current_index=current_index)
            await show_basket_item(callback.message, bot, current_index, state, mode="+-1")
            
            await callback.answer("Количество товара изменено")
        else:
            db.remove_product_from_basket(user_id, product_id)
            basket.pop(current_index)
            if current_index == len(basket):
                current_index -= 1
            
            await state.update_data(basket=basket, current_index=current_index)
            await show_basket_item(callback.message, bot, current_index, state, mode="delete")
            
            await callback.answer("Товар удален из корзины")
    elif "Удалить_" in choice:
        db.remove_product_from_basket(user_id, product_id)
        basket.pop(current_index)
        if current_index == len(basket):
            current_index -= 1
        
        await state.update_data(basket=basket, current_index=current_index)
        if len(basket) == 0:
            data = await state.get_data()
            last_basket_msg = data.get("last_basket_msg_id")
            await bot.edit_message_reply_markup(
                chat_id=callback.message.chat.id,
                message_id=last_basket_msg,
                reply_markup=None
            )
        await show_basket_item(callback.message, bot, current_index, state, mode="delete")
        
        await callback.answer("Товар удален из корзины")
            

@basket_router.message(MainState.view_basket, F.text.func(TextNormalizer("очистить корзину")))
async def clear_basket(message: types.Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    last_basket_msg_id = data.get("last_basket_msg_id")
    if last_basket_msg_id:
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=last_basket_msg_id,
            reply_markup=None
        )
        await state.update_data(last_basket_msg_id=None)
    
    db.clear_basket(message.from_user.id)
    await message.answer("Корзина очищена!")


# Функция для выбора даты доставки
@basket_router.message(MainState.view_basket, F.text.func(TextNormalizer("оформить заказ")))
async def select_data(message: types.Message, state: FSMContext):
    if not db.get_basket(message.from_user.id):
        await message.answer(
            "Ваша корзина пуста!\n"
            "Для оформления заказа добавьте хотя бы один товар в корзину."
        )
        return
    
    calendar = ac.SimpleCalendar(
        cancel_btn="Отмена",
        today_btn="Сегодня"
    )
    await message.answer(
        text="Для оформления заказа выберите дату и время доставки",
        reply_markup=cancel_delivery
    )
    await message.answer(
        "Выберите дату доставки",
        reply_markup=await calendar.start_calendar()
    )
    await state.set_state(MainState.choose_time_delivery)


# Функция для выбора даты доставки
@basket_router.callback_query(MainState.choose_time_delivery, ac.SimpleCalendarCallback.filter())
async def get_date_delivery(callback_query: types.CallbackQuery, callback_data: ac.SimpleCalendarCallback, state: FSMContext):
    selected, date = await ac.SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        calendar = ac.SimpleCalendar(
            cancel_btn="Отмена",
            today_btn="Сегодня"
        )
        
        date_now = datetime.now()
        date_max = date_now + timedelta(days=60)
        
        if date > date_max:
            await callback_query.message.answer(
                "Срок доставки должен быть меньше 60 дней.\n"
                "Пожалуйста, выберите другую дату",
                reply_markup=await calendar.start_calendar()
            )
            return
        elif date <= date_now:
            await callback_query.message.answer(
                "Заказ можно оформить только на завтра или позже.\n"
                "Пожалуйста, выберите другую дату",
                reply_markup=await calendar.start_calendar()
            )
            return
        
        msg = await callback_query.message.answer(
            f"Вы выбрали: {date.strftime('%d.%m.%Y')}\n"
            f"Выберите время доставки",
            reply_markup=get_delivery_time_kb()
        )
        await state.set_state(MainState.confirm_delivery)
        await state.update_data(last_delivery_msg=msg.message_id, date=date)
    else:
        await callback_query.answer("Выберите дату из календаря")


# Функция для выбора времени доставки
@basket_router.callback_query(MainState.confirm_delivery)
async def get_time_delivery(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    last_delivery_msg = data.get("last_delivery_msg")
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=last_delivery_msg,
        reply_markup=None
    )
    await callback.message.answer(
        text=f"Вы выбрали {callback.data}"
    )   
    
    data = await state.get_data()
    date = data.get("date")
    await callback.message.answer(
        text=f"Дата и время доставки: {date.strftime('%d.%m.%Y')}, {callback.data}.",
        reply_markup=confirm_delivery
    )
       
    await state.update_data(time=callback.data)
    
    

# Функция для подтверждения даты и времени доставки
@basket_router.message(MainState.confirm_delivery, F.text.func(TextNormalizer("подтвердить")))
async def get_confirm_delivery(message: types.Message, state: FSMContext):
    data = await state.get_data()
    date = data.get("date")
    time = data.get("time")
    db.add_order(message.from_user.id, date, time)
    db.clear_basket(message.from_user.id)
    
    menu = seller_main_menu if message.from_user.id in db.sellers else user_main_menu
    await message.answer("Заказ успешно оформлен! Ожидайте.", reply_markup=menu)
    await state.set_state(MainState.view_main)


# Функция для отмены оформления заказа
@basket_router.message(StateFilter(MainState.choose_time_delivery, MainState.confirm_delivery),
                       F.text.func(TextNormalizer("отмена")))
async def get_cancel_delivery(message: types.Message, state: FSMContext):
    menu = seller_main_menu if message.from_user.id in db.sellers else user_main_menu
    await message.answer("Возвращаю в главное меню...", reply_markup=menu)
    await state.set_state(MainState.view_main)