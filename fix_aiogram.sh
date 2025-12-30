#!/bin/bash
echo "Обновление для aiogram 3.7+..."

# 1. Обновляем main.py
cat > src/main.py << 'PYEOF'
import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("=== Gym Delivery Bot ===")

    try:
        # Import settings
        from src.config import settings
        logger.info("✅ Конфигурация загружена")

        # Check bot token
        if not settings.bot.token or settings.bot.token == "your_bot_token_here":
            logger.error("❌ Установи BOT_TOKEN в файле .env")
            logger.error("   Получите токен у @BotFather")
            logger.error("   Пример: BOT_TOKEN=1234567890:ABCdefGHIjklMNoPQRstUVwxyz")
            return

        logger.info(f"✅ Токен получен: {settings.bot.token[:10]}...")

        # Show admin IDs
        if settings.bot.admin_ids:
            logger.info(f"✅ Админы: {settings.bot.admin_ids}")
        else:
            logger.info("✅ Админы не настроены")

        # Database
        logger.info(f"✅ База данных: {settings.database.database}")

        # i18n
        logger.info(f"✅ Языки: {settings.localization.supported_languages}")

        # Start bot
        logger.info("🚀 Запускаем бота...")

        # Import and start bot
        from aiogram import Bot, Dispatcher
        from aiogram.fsm.storage.memory import MemoryStorage
        from aiogram.client.default import DefaultBotProperties

        # Правильное создание бота для aiogram 3.7+
        bot = Bot(
            token=settings.bot.token,
            default=DefaultBotProperties(parse_mode="HTML")
        )
        dp = Dispatcher(storage=MemoryStorage())

        # Import handlers
        from src.api.handlers.start import router as start_router
        from src.api.handlers.language import router as language_router
        dp.include_router(start_router)
        dp.include_router(language_router)

        # Set bot commands
        from aiogram.types import BotCommand
        commands = [
            BotCommand(command="start", description="🚀 Запустить бота"),
            BotCommand(command="help", description="ℹ️ Помощь"),
            BotCommand(command="language", description="🌐 Сменить язык"),
        ]
        await bot.set_my_commands(commands)

        logger.info("🤖 Бот успешно запущен!")
        logger.info("Остановите бота комбинацией Ctrl+C")

        await dp.start_polling(bot)

    except ImportError as e:
        logger.error(f"❌ Ошибка импорта: {e}")
        logger.error("Проверьте структуру проекта и установленные зависимости")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
PYEOF

# 2. Создаем language.py
cat > src/api/handlers/language.py << 'PYEOF'
from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()


@router.message(Command("language"))
async def cmd_language(message: types.Message):
    """Обработчик команды /language"""

    from src.infrastructure.i18n.service import i18n_service

    # Получаем доступные языки
    languages = i18n_service.get_supported_languages()

    # Создаем клавиатуру для выбора языка
    from aiogram.utils.keyboard import InlineKeyboardBuilder

    builder = InlineKeyboardBuilder()
    for lang_code, lang_name in languages.items():
        builder.button(
            text=lang_name,
            callback_data=f"lang_{lang_code}"
        )
    builder.adjust(2)

    await message.answer(
        "🌐 Выберите язык интерфейса:\n\n"
        "🌐 Choose interface language:\n\n"
        "🌐 Интерфейс тилини танланг:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("lang_"))
async def select_language(callback: types.CallbackQuery):
    """Обработчик выбора языка"""
    language_code = callback.data.split("_")[1]

    # Пока просто подтверждаем выбор
    await callback.message.edit_text(
        f"✅ Язык изменен на {language_code.upper()}\n\n"
        f"Перезапустите бота командой /start"
    )
    await callback.answer()
PYEOF

# 3. Обновляем __init__.py
cat > src/api/handlers/__init__.py << 'PYEOF'
from .start import router as start_router
from .language import router as language_router

__all__ = ['start_router', 'language_router']
PYEOF

# 4. Обновляем bot.py
cat > src/bot.py << 'PYEOF'
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.infrastructure.i18n.middleware import I18nMiddleware
from src.api.handlers import (
    start,
    language
)


async def setup_bot(dp: Dispatcher, bot: Bot):
    """Setup bot with all handlers and middleware"""

    # Create main router
    main_router = Router()

    # Include all routers
    main_router.include_router(start.router)
    main_router.include_router(language.router)

    # Setup middleware
    dp.update.middleware(I18nMiddleware())

    # Database middleware
    dp.update.middleware(DatabaseMiddleware())

    # Include main router
    dp.include_router(main_router)

    # Set bot commands
    await set_bot_commands(bot)


async def set_bot_commands(bot: Bot):
    """Set bot commands menu"""
    from aiogram.types import BotCommand

    commands = [
        BotCommand(command="start", description="🚀 Start bot"),
        BotCommand(command="help", description="ℹ️ Help"),
        BotCommand(command="language", description="🌐 Change language"),
    ]

    await bot.set_my_commands(commands)


class DatabaseMiddleware:
    """Middleware for database session"""

    async def __call__(self, handler, event, data):
        async for session in get_session():
            data["session"] = session
            return await handler(event, data)
PYEOF

echo "✅ Все файлы обновлены для aiogram 3.7+"
echo "Перезапустите бота: docker-compose restart bot"