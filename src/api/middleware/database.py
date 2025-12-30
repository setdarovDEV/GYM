from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update
import logging

from src.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


class DatabaseMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        async with AsyncSessionLocal() as session:
            data["session"] = session

            try:
                result = await handler(event, data)
                return result
            except Exception as e:
                await session.rollback()
                logger.error(f"Database error in middleware: {e}", exc_info=True)
                raise
            finally:
                pass