from aiogram import F
from aiogram.types import Message, CallbackQuery

from app.bot.buttons.inline import menu_inline_buttons
from app.bot.buttons.reply import menu_buttons
from app.dispatcher import dp
from db.models import Product, session


# SMALL DOC for menu
# go to zfr_nshnv_bot on telegram
# input '🥗 Menyu' and you will get 3 reply buttons

@dp.message(F.text == '🥗 Menyu')
async def menu_handler(message: Message):
    menu = menu_buttons()
    await message.answer(text='success', reply_markup=menu)

@dp.message(F.text == "Barcha maxsulotlar")
async def full_menu_handler(message: Message):
    foods = session.query(Product).all()
    btns = [(food.name, f"food_{food.id}") for food in foods]
    barchasi = menu_inline_buttons(btns, [1], True)
    await message.answer(text="Barcha taomlar", reply_markup=barchasi)

@dp.message(F.text == '🔥 Ozish')
async def ozish_handler(message: Message):
    ozishfood = session.query(Product).filter(Product.category_id == 1).all()
    btns = [(food.name, f"food_{food.id}") for food in ozishfood]
    ozish = menu_inline_buttons(btns, [1], True)
    await message.answer(text='Ozish uchun kopro sport bilan shugullanish kere', reply_markup=ozish)

@dp.message(F.text == '💪 Semirish')
async def semirish_handler(message: Message):
    semirishfood = session.query(Product).filter(Product.category_id == 2).all()
    btns = [(food.name, f"food_{food.id}") for food in semirishfood]
    semirish = menu_inline_buttons(btns, [1], True)
    await message.answer(text="Semirish uchun kopro ovqat yiyish kere", reply_markup=semirish)

@dp.message(F.text == '🥤 Sport ichimliklari')
async def ichimlik_handler(message: Message):
    drink = session.query(Product).filter(Product.category_id == 3).all()
    btns = [(food.name, f"food_{food.id}") for food in drink]
    ichimlik = menu_inline_buttons(btns, [1], True)
    await message.answer(text="Ichimliklar zarar faqat suv ichish kere", reply_markup=ichimlik)

@dp.callback_query(F.data.startswith("food_"))
async def food_handler(callback: CallbackQuery):
    await callback.message.delete()
    food_id: int = int(callback.data.split("_")[1])
    food = session.query(Product).filter(Product.id == food_id).first()
    print(food.photo)
    caption = f"""{food.name}\n{food.description}\n sotuvda {food.quantity} ta bor \n Narxi {food.price}"""
    btns = [("Savatga qo'shish", f"order_add_{food_id}"), ("🥙 Menyu", "menu")]
    markup = menu_inline_buttons(btns, size=[1], repeat=True)
    await callback.message.answer_photo(photo=food.photo, caption=caption, reply_markup=markup)