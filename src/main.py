import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from src.config import settings
from src.core.database import create_tables
from src.api.middleware.database import DatabaseMiddleware
from src.infrastructure.i18n.middleware import I18nMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="help", description="ℹ️ Помощь"),
        BotCommand(command="language", description="🌐 Сменить язык"),
    ]
    await bot.set_my_commands(commands)
    logger.info("Команды бота установлены")


async def main():
    logger.info("=" * 50)
    logger.info("Запуск Gym Delivery Bot")
    logger.info("=" * 50)

    try:
        if not settings.bot.token or settings.bot.token == "your_bot_token_here":
            logger.error("   BOT_TOKEN не установлен!")
            logger.error("   Получите токен у @BotFather")
            logger.error("   Установите его в файле .env")
            return

        logger.info(f"Токен: {settings.bot.token[:10]}...")

        logger.info(f"База данных: {settings.database.database}")
        logger.info(f"Поддерживаемые языки: {', '.join(settings.localization.supported_languages)}")
        logger.info(f"Язык по умолчанию: {settings.localization.default_language}")

        if settings.bot.admin_ids:
            logger.info(f"Админы: {settings.bot.admin_ids}")

        logger.info("Создание таблиц базы данных...")
        await create_tables()
        logger.info("Таблицы созданы/проверены")

        bot = Bot(
            token=settings.bot.token,
            default=DefaultBotProperties(parse_mode="HTML")
        )

        dp = Dispatcher(storage=MemoryStorage())

        dp.update.middleware(DatabaseMiddleware())
        logger.info("DatabaseMiddleware зарегистрирован")

        dp.update.middleware(I18nMiddleware())
        logger.info("I18nMiddleware зарегистрирован")

        from src.api.handlers.start import router as start_router
        from src.api.handlers.language import router as language_router

        dp.include_router(start_router)
        dp.include_router(language_router)
        logger.info("Обработчики зарегистрированы")

        await set_bot_commands(bot)

        logger.info("=" * 50)
        logger.info("Бот успешно запущен!")
        logger.info("Для остановки нажмите Ctrl+C")
        logger.info("=" * 50)

        await dp.start_polling(bot)

    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
    finally:
        logger.info("Завершение работы бота")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")