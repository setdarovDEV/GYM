from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def menu_buttons():
    ozish = KeyboardButton(text='🔥 Ozish ')
    semirish = KeyboardButton(text='💪 Semirish')
    ichimlik = KeyboardButton(text='🥤 Sport ichimliklari')
    reply = ReplyKeyboardBuilder()
    reply.add(ozish, semirish, ichimlik)
    reply.adjust(3)
    return reply.as_markup(resize_keyboard=True)