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

    main_router = Router()

    main_router.include_router(start.router)
    main_router.include_router(language.router)

    dp.update.middleware(I18nMiddleware())

    dp.update.middleware(DatabaseMiddleware())

    dp.include_router(main_router)

    await set_bot_commands(bot)


async def set_bot_commands(bot: Bot):
    from aiogram.types import BotCommand

    commands = [
        BotCommand(command="start", description="🚀 Start bot"),
        BotCommand(command="help", description="ℹ️ Help"),
        BotCommand(command="language", description="🌐 Change language"),
    ]

    await bot.set_my_commands(commands)


class DatabaseMiddleware:

    async def __call__(self, handler, event, data):
        async for session in get_session():
            data["session"] = session
            return await handler(event, data)