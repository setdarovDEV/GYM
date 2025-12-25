from aiogram.types import Message

from aiogram import F

from app.dispatcher import dp


@dp.message(F.text == "Oxirgi buyurtma")
async def last_orders(message: Message):
    await message.answer("oxirgi buyurtmalar")