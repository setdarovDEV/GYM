from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Callable

from src.domain.users.models import User
from src.api.keyboards.base import get_main_menu_keyboard, get_language_selection_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(
        message: types.Message,
        session: AsyncSession,
        state: FSMContext,
        lang: str,
        _: Callable
):
    await state.clear()

    user_data = message.from_user

    stmt = select(User).where(User.telegram_id == user_data.id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    is_new_user = user is None

    if user:
        user.username = user_data.username
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.language_code = user_data.language_code
        user.is_active = True
    else:
        initial_lang = 'ru'
        if user_data.language_code:
            telegram_lang = user_data.language_code.lower().split('-')[0]
            if telegram_lang in ['ru', 'uz', 'en']:
                initial_lang = telegram_lang

        user = User(
            telegram_id=user_data.id,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            language_code=user_data.language_code,
            language=initial_lang,
            is_active=True
        )
        session.add(user)

    await session.commit()

    user_language = user.language or 'ru'

    if is_new_user:
        welcome_text = (
            "👋 <b>Добро пожаловать в Gym Delivery!</b>\n\n"
            "👋 <b>Gym Delivery ga xush kelibsiz!</b>\n\n"
            "👋 <b>Welcome to Gym Delivery!</b>\n\n"
            "💪 Мы доставляем спортивное питание\n"
            "💪 Biz sport ovqatlanishini yetkazib beramiz\n"
            "💪 We deliver sports nutrition\n\n"
            "🌐 Пожалуйста, выберите язык:\n"
            "🌐 Iltimos, tilni tanlang:\n"
            "🌐 Please choose language:"
        )

        await message.answer(
            welcome_text,
            reply_markup=get_language_selection_keyboard(current_lang=None)
        )
    else:
        name = user_data.first_name or "друг"
        welcome_text = _("welcome.returning", name=name)

        await message.answer(
            welcome_text,
            reply_markup=get_main_menu_keyboard(user_language)
        )


@router.message(Command("help"))
@router.message(F.text.in_(["ℹ️ Помощь", "ℹ️ Yordam", "ℹ️ Help"]))
async def cmd_help(
        message: types.Message,
        _: Callable,
        lang: str
):

    help_text = (
        f"<b>{_('commands.help')}</b>\n\n"
        f"📦 {_('commands.catalog')} - /catalog\n"
        f"🛒 {_('commands.cart')} - /cart\n"
        f"📋 {_('commands.orders')} - /orders\n"
        f"👤 {_('commands.profile')} - /profile\n"
        f"🌐 {_('commands.language')} - /language\n\n"
        f"💡 <b>Контакты:</b>\n"
        f"📱 Телефон: +998 90 123 45 67\n"
        f"📧 Email: support@gymdelivery.uz\n"
        f"⏰ Работаем: 09:00 - 22:00"
    )

    await message.answer(help_text)


@router.message(F.text.in_(["🏠 В главное меню", "🏠 Asosiy menyuga", "🏠 Main Menu"]))
async def back_to_menu(
        message: types.Message,
        _: Callable,
        lang: str
):

    await message.answer(
        _("main_menu.title"),
        reply_markup=get_main_menu_keyboard(lang)
    )