from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.buttons.reply import start_button
from app.dispatcher import dp

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    buttons = start_button()
    await message.answer(f"Hello", reply_markup=buttons)
