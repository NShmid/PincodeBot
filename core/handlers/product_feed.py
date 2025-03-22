from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from core.keyboards.reply_keyboards import user_main_menu, basket_menu
from core.keyboards.inline_keyboards import get_product_feed_keyboard, get_basket_keyboard
from core.keyboards.reply_keyboards import product_menu
from core.database import db
from core.utils.main_state import MainState, offset


product_feed_router = Router()


# Функция для отображения ленты
async def show_products(message: types.Message, products):
    for product in products:
        product_id = product[0]
        product_name = product[1]
        product_descr = product[2]
        product_count = product[3]
        product_price = product[4]
        product_image = types.FSInputFile(f"images/{product_id}.jpg")
        
        caption = (f"<b>{product_name}</b>\n"
        f"Описание: {product_descr}\n"
        f"Количество: {product_count}\n"
        f"Цена: {product_price}")
        
        await message.answer_photo(photo=product_image, caption=caption, parse_mode="HTML",
                                    reply_markup=get_product_feed_keyboard(product_id))


# Функция для отображения ленты в первый раз
@product_feed_router.message(F.text.lower() == "лента товаров")
async def get_product_feed(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    offset[user_id] = 0
    
    # Первые 7 товаров:
    products = db.get_products(offset=offset[user_id])
    
    await message.answer("Загружаю ленту товаров...", reply_markup=product_menu)
    
    if products:
        await show_products(message, products)
            
        await state.set_state(MainState.view_products)
            
        offset[user_id] += 7
    else:
        await message.answer("Больше нет товаров")
        
        
# Функция для отображения ленты на кнопку "еще"
@product_feed_router.message(MainState.view_products, F.text.lower() == "еще товары")
async def show_product_feed(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    products = db.get_products(offset=offset[user_id])
    
    if products:
        await show_products(message, products)
        
        offset[user_id] += 7
    else:
        await message.answer("Больше нет товаров")
        

# Функция для возврата в главное меню
@product_feed_router.message(MainState.view_products, F.text.lower() == "главное меню")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await message.answer("Возвращаю в главное меню...", reply_markup=user_main_menu)
    await state.clear()


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


# Функция для просмотра корзины
@product_feed_router.message(MainState.view_products, F.text.lower() == "корзина")
async def get_basket(message: types.Message, state: FSMContext):   
    user_id = message.from_user.id
    basket = db.get_basket(user_id)
    
    await state.set_state(MainState.view_basket)
    await state.update_data(basket=basket)
    await show_basket_item(message, 0, state)
    

# Функция для кнопок "Далее" и "Назад" в корзине
@product_feed_router.callback_query(MainState.view_basket)
async def process_next(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data.get("current_index")
    basket = data.get("basket")
    
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


# Функция для обработки инлайн кнопок в ленте
@product_feed_router.callback_query(MainState.view_products)
async def add_product_to_basket(callback: types.CallbackQuery):
    choice = callback.data
    user_id = callback.from_user.id
    
    product_id = int(choice.replace("add_to_basket_", "").strip()) # id выбранного продукта
    product = db.get_product(product_id)
    
    if "add_to_basket_" in choice:
        db.add_product_to_basket(user_id, product_id)
        
        await callback.answer(f"Товар \"{product[0][1]}\" успешно добавлен в корзину")
        
    elif "preorder_" in choice:
        await callback.answer(f"Вы оформили предзаказ на товар \"{product[0][1]}\"")