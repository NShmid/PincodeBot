from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from core.keyboards.inline_keyboards import get_user_product_feed_keyboard, get_admin_product_feed_keyboard
from core.keyboards.reply_keyboards import product_menu
from core.database import db
from core.utils.main_state import MainState, offset
from core.filters.emoji_filter import TextNormalizer


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
        
        user_id = message.from_user.id
        keyboard = get_user_product_feed_keyboard(product_id)
        if user_id in db.admins:
            keyboard = get_admin_product_feed_keyboard(product_id)
        await message.answer_photo(photo=product_image, caption=caption, parse_mode="HTML",
                                    reply_markup=keyboard)


# Функция для отображения ленты в первый раз
@product_feed_router.message(StateFilter(MainState.view_main, MainState.view_basket),
                             F.text.func(TextNormalizer("лента товаров")))
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
@product_feed_router.message(MainState.view_products, F.text.func(TextNormalizer("еще товары")))
async def show_product_feed(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    products = db.get_products(offset=offset[user_id])
    
    if products:
        await show_products(message, products)
        
        offset[user_id] += 7
    else:
        await message.answer("Больше нет товаров")
        

# Функция для обработки инлайн кнопок в ленте
@product_feed_router.callback_query(MainState.view_products)
async def add_product_to_basket(callback: types.CallbackQuery):
    choice = callback.data
    user_id = callback.from_user.id
    
    if "add_to_basket_" in choice:
        product_id = int(choice.replace("add_to_basket_", "").strip()) # id выбранного продукта
        product = db.get_product(product_id)
        db.add_product_to_basket(user_id, product_id)
        
        await callback.answer(f"Товар \"{product[0][1]}\" успешно добавлен в корзину")
        
    elif "preorder_" in choice:
        product_id = int(choice.replace("preorder_", "").strip()) # id выбранного продукта
        product = db.get_product(product_id)
        await callback.answer(f"Вы оформили предзаказ на товар \"{product[0][1]}\"")
    
    elif "delete_" in choice:
        product_id = int(choice.replace("delete_", "").strip()) # id выбранного продукта
        product = db.get_product(product_id)
        await callback.answer(f"Вы удалили товар \"{product[0][1]}\"")