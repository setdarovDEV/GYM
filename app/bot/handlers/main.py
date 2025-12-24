from aiogram.filters import CommandStart
from aiogram.types import Message

from app.dispatcher import dp

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello")
