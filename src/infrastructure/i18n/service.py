import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.users.models import User
from src.config import settings

logger = logging.getLogger(__name__)


class I18nService:

    def __init__(self):
        self._translations: Dict[str, Dict[str, str]] = {}
        self._supported_languages = settings.localization.supported_languages
        self._default_language = settings.localization.default_language
        self._locales_path = Path(settings.localization.locales_path)

        self._user_lang_cache: Dict[int, str] = {}

        self._flags = {
            "ru": "🇷🇺",
            "uz": "🇺🇿",
            "en": "🇬🇧"
        }

        self._load_translations()

    def _load_translations(self) -> None:
        logger.info(f"Loading translations from: {self._locales_path}")

        for lang in self._supported_languages:
            file_path = self._locales_path / f"{lang}.json"

            if not file_path.exists():
                logger.warning(f"Translation file not found: {file_path}")
                self._translations[lang] = {}
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self._translations[lang] = json.load(f)
                logger.info(f"✅ Loaded {lang}: {len(self._translations[lang])} keys")
            except Exception as e:
                logger.error(f"Failed to load {lang}: {e}")
                self._translations[lang] = {}

    def get(self, key: str, lang: str, **kwargs) -> str:
        if lang not in self._translations:
            lang = self._default_language

        translation = self._get_nested_value(self._translations[lang], key)

        if translation is None and lang != self._default_language:
            translation = self._get_nested_value(
                self._translations[self._default_language],
                key
            )

        if translation is None:
            logger.warning(f"Translation not found: {key} for lang: {lang}")
            return key

        if kwargs:
            try:
                return translation.format(**kwargs)
            except KeyError as e:
                logger.warning(f"Missing format parameter {e} for key: {key}")
                return translation

        return translation

    def _get_nested_value(self, data: Dict, key: str) -> Optional[str]:
        keys = key.split('.')
        value = data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None

        return value if isinstance(value, str) else None

    async def get_user_language(
            self,
            user_id: int,
            session: AsyncSession
    ) -> str:
        if user_id in self._user_lang_cache:
            return self._user_lang_cache[user_id]

        try:
            stmt = select(User.language).where(User.telegram_id == user_id)
            result = await session.execute(stmt)
            lang = result.scalar_one_or_none()

            if lang and lang in self._supported_languages:
                self._user_lang_cache[user_id] = lang
                return lang

            return self._default_language

        except Exception as e:
            logger.error(f"Error getting user language: {e}")
            return self._default_language

    async def set_user_language(
            self,
            user_id: int,
            lang: str,
            session: AsyncSession
    ) -> bool:
        if lang not in self._supported_languages:
            logger.warning(f"Unsupported language: {lang}")
            return False

        try:
            stmt = select(User).where(User.telegram_id == user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                user.language = lang
                await session.commit()

                self._user_lang_cache[user_id] = lang
                logger.info(f"Language updated for user {user_id}: {lang}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error setting user language: {e}")
            await session.rollback()
            return False

    def get_supported_languages(self) -> Dict[str, str]:
        result = {}
        for lang in self._supported_languages:
            flag = self._flags.get(lang, "🏳️")
            name = self.get("language_name", lang)
            result[lang] = f"{flag} {name}"
        return result

    def clear_cache(self, user_id: Optional[int] = None) -> None:
        if user_id:
            self._user_lang_cache.pop(user_id, None)
        else:
            self._user_lang_cache.clear()


i18n_service = I18nService()