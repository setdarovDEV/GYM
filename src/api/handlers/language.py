from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable

from src.infrastructure.i18n.service import i18n_service
from src.api.keyboards.base import get_main_menu_keyboard

router = Router()


@router.message(Command("language"))
@router.message(F.text.in_(["Язык", "Til", "Language", "Настройки", "Sozlamalar", "Settings"]))
async def cmd_language(
        message: types.Message,
        _: Callable,
        lang: str
):

    current_lang = lang

    languages = i18n_service.get_supported_languages()

    builder = InlineKeyboardBuilder()
    for lang_code, lang_display in languages.items():
        if lang_code == current_lang:
            lang_display = f"{lang_display}"

        builder.button(
            text=lang_display,
            callback_data=f"lang_{lang_code}"
        )

    builder.adjust(2)

    text = (
        "🌐 <b>Выберите язык / Tilni tanlang / Choose language</b>\n\n"
        "Ваш текущий язык / Joriy til / Current language:\n"
        f"➡️ <b>{languages.get(current_lang, 'Русский')}</b>"
    )

    await message.answer(
        text,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("lang_"))
async def callback_language(
        callback: types.CallbackQuery,
        session: AsyncSession,
        _: Callable,
        lang: str
):

    new_lang = callback.data.split("_")[1]
    user_id = callback.from_user.id

    if new_lang == lang:
        await callback.answer("Это уже ваш текущий язык")
        return

    success = await i18n_service.set_user_language(user_id, new_lang, session)

    if success:
        def new_translate(key: str, **kwargs) -> str:
            return i18n_service.get(key, new_lang, **kwargs)

        confirmation_text = new_translate("welcome.language_selected")

        await callback.message.edit_text(
            f"✅ {confirmation_text}\n\n"
            f"Используйте /start для обновления меню"
        )

        await callback.message.answer(
            new_translate("main_menu.title"),
            reply_markup=get_main_menu_keyboard(new_lang)
        )

        await callback.answer()
    else:
        await callback.answer("Ошибка при смене языка", show_alert=True)