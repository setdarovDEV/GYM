from aiogram import F
from aiogram.types import Message

from app.bot.buttons.inline import menu_inline_buttons
from app.bot.buttons.reply import menu_buttons
from app.dispatcher import dp

# SMALL DOC for menu
# go to zfr_nshnv_bot on telegram
# input '🥗 Menyu' and you will get 3 reply buttons

@dp.message(F.text == '🥗 Menyu')
async def menu_handler(message: Message):
    menu = menu_buttons()
    await message.answer(text='success', reply_markup=menu)

@dp.message(F.text == '🔥 Ozish')
async def ozish_handler(message: Message):
    btns = [('Salat', '1'), ('Tovuq', '2'), ('Olma','3')]
    ozish = menu_inline_buttons(btns, [1], True)
    await message.answer(text='Ozish uchun kopro sport bilan shugullanish kere', reply_markup=ozish)

@dp.message(F.text == '💪 Semirish')
async def semirish_handler(message: Message):
    btns = [('Mol goshti', '4'), ('Grechka', '5'), ('Avokado', '6')]
    semirish = menu_inline_buttons(btns, [1], True)
    await message.answer(text="Semirish uchun kopro ovqat yiyish kere", reply_markup=semirish)

@dp.message(F.text == '🥤 Sport ichimliklari')
async def ichimlik_handler(message: Message):
    btns = [('Suv', '7'), ('Kokteyl', '8'), ('RedBull', '9')]
    ichimlik = menu_inline_buttons(btns, [1], True)
    await message.answer(text="Ichimliklar zarar faqat suv ichish kere", reply_markup=ichimlik)