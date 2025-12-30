from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton
)
from typing import Optional, List

from src.infrastructure.i18n.service import i18n_service


def get_main_menu_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    catalog_text = i18n_service.get("buttons.catalog", language)
    cart_text = i18n_service.get("buttons.cart", language, count=0)
    orders_text = i18n_service.get("buttons.orders", language)
    profile_text = i18n_service.get("buttons.profile", language)
    settings_text = i18n_service.get("buttons.settings", language)

    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=catalog_text),
        KeyboardButton(text=cart_text)
    )

    builder.row(
        KeyboardButton(text=orders_text),
        KeyboardButton(text=profile_text)
    )

    builder.row(
        KeyboardButton(text=settings_text)
    )

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder=i18n_service.get("main_menu.choose_action", language)
    )


def get_language_selection_keyboard(
        current_lang: Optional[str] = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    languages = i18n_service.get_supported_languages()

    for lang_code, lang_display in languages.items():
        if lang_code == current_lang:
            lang_display = f"✅ {lang_display}"

        builder.button(
            text=lang_display,
            callback_data=f"lang_{lang_code}"
        )

    builder.adjust(2)

    return builder.as_markup()


def get_back_button(language: str = "ru", callback_data: str = "back") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n_service.get("buttons.back", language),
        callback_data=callback_data
    )
    return builder.as_markup()


def get_cancel_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n_service.get("buttons.cancel", language),
        callback_data="cancel"
    )
    return builder.as_markup()


def get_confirm_cancel_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=i18n_service.get("buttons.confirm", language),
            callback_data="confirm"
        ),
        InlineKeyboardButton(
            text=i18n_service.get("buttons.cancel", language),
            callback_data="cancel"
        )
    )
    return builder.as_markup()


def get_share_phone_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(
            text=i18n_service.get("buttons.share_phone", language),
            request_contact=True
        )
    )
    builder.row(
        KeyboardButton(text=i18n_service.get("buttons.cancel", language))
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_share_location_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(
            text=i18n_service.get("buttons.share_location", language),
            request_location=True
        )
    )
    builder.row(
        KeyboardButton(text=i18n_service.get("buttons.cancel", language))
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)