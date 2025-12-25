from aiogram.types import Message

from aiogram import F
from sqlalchemy.sql import select
from app.dispatcher import dp
from db.models import Order, session


@dp.message(F.text == "📜 Oxirgi Buyurtma")
async def last_orders(message: Message):
    last_order_view = (select(Order).filter_by(user_id=message.from_user.id).order_by(Order.id.desc()).limit(5))
    result = session.execute(last_order_view).scalars().all()
    text = "Oxirgi Buyurtmalar:\n"

    if not result:
        await message.answer("sizda buyurtmalar yo'q")
        return
    for res in result:
        text += f"ID: {res.id}\n"
        text += f"Name: {res.name}\n"
        text += f"Price: {res.price}\n"
    await message.answer(text)