from aiogram import F
from aiogram.types import Message

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
    await message.answer(text='Ozish uchun kopro sport bilan shugullanish kere')

@dp.message(F.text == '💪 Semirish')
async def semirish_handler(message: Message):
    await message.answer(text="Semirish uchun kopro ovqat yiyish kere")

@dp.message(F.text == '🥤 Sport ichimliklari')
async def ichimlik_handler(message: Message):
    await message.answer(text="Ichimliklar zarar faqat suv ichish kere")