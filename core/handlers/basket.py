from core.database import db
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from core.keyboards.reply_keyboards import user_main_menu, basket_menu
from core.keyboards.inline_keyboards import get_basket_keyboard
from core.keyboards.reply_keyboards import product_menu
from core.database import db
from core.utils.main_state import MainState


basket_router = Router()


# Функция для отображения одного товара из корзины
async def show_basket_item(message: types.Message, current_index: int, state: FSMContext):
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
    
    await message.answer_photo(photo=product_image, caption=caption, parse_mode="HTML",
                         reply_markup=get_basket_keyboard(current_index, len(basket), product_id))
    
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
    
    await message.answer(answer, reply_markup=basket_menu, parse_mode="HTML")


# Функция для просмотра корзины из ленты или из главного меню
@basket_router.message(StateFilter(MainState.view_products, MainState.view_main), F.text.lower() == "корзина")
async def get_basket(message: types.Message, state: FSMContext):   
    user_id = message.from_user.id
    basket = db.get_basket(user_id)
    
    await state.set_state(MainState.view_basket)
    await state.update_data(basket=basket)
    await state.update_data(current_index=0)
    await show_basket_item(message, 0, state)
    

# Функция для инлайн кнопок в корзине
@basket_router.callback_query(MainState.view_basket)
async def redo_undo_basket(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data.get("current_index")
    basket = data.get("basket")
    product_id, count = basket[current_index]
    user_id = callback.from_user.id
    
    choice = callback.data
    if "Далее_" in choice:
        if current_index < len(basket) - 1:
            current_index += 1
            await show_basket_item(callback.message, current_index, state)
        
        await callback.answer()  # Закрываем callback
    elif "Назад_" in choice:
        if current_index > 0:
            current_index -= 1
            await show_basket_item(callback.message, current_index, state)
    
        await callback.answer()  # Закрываем callback
    elif "+1_" in choice:
        product_count = db.get_product(product_id)[0][-2]
        if count <= product_count:
            db.adding_one(user_id, product_id)
            basket[current_index] = basket[current_index][0], basket[current_index][-1] + 1
            await state.update_data(basket=basket)
            await show_basket_item(callback.message, current_index, state)
            await callback.answer("Количество товара изменено")
        else:
            await callback.answer("Вы не можете больше добавить этот товар")
        
    elif "-1_" in choice:
        if count > 1:
            db.subtraction_one(user_id, product_id)
            basket[current_index] = basket[current_index][0], basket[current_index][-1] - 1
            await state.update_data(basket=basket, current_index=current_index)
            await show_basket_item(callback.message, current_index, state)
            
            await callback.answer("Количество товара изменено")
        else:
            db.remove_product_from_basket(user_id, product_id)
            if current_index == len(basket) - 1:
                current_index -= 1
            
            basket.remove(basket[current_index])
            await state.update_data(basket=basket, current_index=current_index)
            await show_basket_item(callback.message, current_index, state)
            
            await callback.answer("Товар удален из корзины")
            

# Функция для оформления заказа
@basket_router.message(MainState.view_basket, F.text.lower() == "оформить заказ")
async def redo_undo_basket(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    db.clear_basket(user_id)
    await message.answer("Заказ оформлен, ожидайте.")