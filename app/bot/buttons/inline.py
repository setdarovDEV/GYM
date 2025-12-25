from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu_inline_buttons(btns, size, repeat=False):
    reply = InlineKeyboardBuilder()
    reply.add(*[InlineKeyboardButton(text=text, callback_data=callback) for text, callback in btns])
    reply.adjust(*size, repeat=repeat)
    return reply.as_markup()