from aiofiles.os import replace
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def start_button():
    menyu = KeyboardButton(text='🥗 Menyu')
    profilim = KeyboardButton(text='👤 Profilim ')
    savat = KeyboardButton(text='🛒 Savat')
    oxirgi = KeyboardButton(text='📜 Oxirgi Buyurtma')
    reply = ReplyKeyboardBuilder()
    reply.add(menyu, profilim, savat, oxirgi)
    reply.adjust(2, 2)
    return reply.as_markup(resize_keyboard=True)

def menu_buttons():
    ozish = KeyboardButton(text='🔥 Ozish ')
    semirish = KeyboardButton(text='💪 Semirish')
    ichimlik = KeyboardButton(text='🥤 Sport ichimliklari')
    barchasi = KeyboardButton(text='Barcha maxsulotlar')
    reply = ReplyKeyboardBuilder()
    reply.add(ozish, semirish, ichimlik, barchasi)
    reply.adjust(3)
    return reply.as_markup(resize_keyboard=True)