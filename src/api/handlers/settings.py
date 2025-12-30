from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.models import User
from src.api.keyboards.base import (
    get_settings_keyboard,
    get_language_selection_keyboard,
    get_back_to_settings_keyboard
)

router = Router()


@router.message(Command("language"))
@router.message(F.text.contains("🌐"))
async def cmd_language(
    message: types.Message,
    _,
    lang: str
):
    text = _("settings.language_title")
    await message.answer(
        text,
        reply_markup=get_language_selection_keyboard(current_lang=lang)
    )


@router.message(Command("settings"))
@router.message(F.text.contains("⚙️"))
async def cmd_settings(
    message: types.Message,
    _,
    lang: str
):
    text = _("settings.title")
    await message.answer(
        text,
        reply_markup=get_settings_keyboard(_)
    )


@router.callback_query(F.data == "back_to_settings")
async def back_to_settings(
    callback: types.CallbackQuery,
    _,
    lang: str
):
    text = _("settings.title")
    await callback.message.edit_text(
        text,
        reply_markup=get_settings_keyboard(_)
    )
    await callback.answer()