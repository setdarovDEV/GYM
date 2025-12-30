from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.infrastructure.i18n.service import i18n_service

logger = logging.getLogger(__name__)


class I18nMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = data.get("session")

        if not session:
            logger.warning("No database session in middleware data")
            data["lang"] = "ru"
            data["_"] = lambda key, **kwargs: i18n_service.get(key, "ru", **kwargs)
            return await handler(event, data)

        user_id = None
        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id

        if not user_id:
            data["lang"] = "ru"
            data["_"] = lambda key, **kwargs: i18n_service.get(key, "ru", **kwargs)
            return await handler(event, data)

        try:
            lang = await i18n_service.get_user_language(user_id, session)
        except Exception as e:
            logger.error(f"Error getting user language: {e}")
            lang = "ru"

        data["lang"] = lang
        data["_"] = lambda key, **kwargs: i18n_service.get(key, lang, **kwargs)

        return await handler(event, data)

i18n_middleware = I18nMiddleware