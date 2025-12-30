import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass

from src.config import settings

logger = logging.getLogger(__name__)


@dataclass
class TranslationKey:
    path: str
    value: str


class I18nLoader:

    def __init__(self):
        self.locales_path = Path(settings.localization.locales_path)
        self._translations: Dict[str, Dict[str, Any]] = {}
        self._flat_translations: Dict[str, Dict[str, str]] = {}
        self.supported_languages = settings.localization.supported_languages
        self.default_language = settings.localization.default_language
        self.fallback_language = settings.localization.fallback_language

        self._load_all_locales()

    def _load_all_locales(self) -> None:
        logger.info(f"Loading locales from: {self.locales_path}")

        for lang in self.supported_languages:
            self._load_locale(lang)

        if self.default_language not in self._translations:
            logger.error(f"Default language '{self.default_language}' not loaded!")
            raise ValueError(f"Default language '{self.default_language}' not found")

    def _load_locale(self, lang: str) -> None:
        file_path = self.locales_path / f"{lang}.json"

        if not file_path.exists():
            logger.warning(f"Locale file not found: {file_path}")
            self._translations[lang] = {}
            self._flat_translations[lang] = {}
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._translations[lang] = self._flatten_to_nested(data)
                self._flat_translations[lang] = data
                logger.info(f"Loaded locale: {lang} ({len(data)} keys)")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in locale file {file_path}: {e}")
            self._translations[lang] = {}
            self._flat_translations[lang] = {}
        except Exception as e:
            logger.error(f"Failed to load locale {lang}: {e}")
            self._translations[lang] = {}
            self._flat_translations[lang] = {}

    def _flatten_to_nested(self, flat_dict: Dict[str, str]) -> Dict[str, Any]:
        result = {}
        for key, value in flat_dict.items():
            parts = key.split('.')
            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        return result

    def get(self, key: str, lang: str, default: Optional[str] = None, **kwargs) -> str:
        target_lang = lang if self.has_language(lang) else self.default_language

        value = self._get_nested(self._translations[target_lang], key)

        if value is None and target_lang != self.fallback_language:
            value = self._get_nested(self._translations.get(self.fallback_language, {}), key)

        if value is None:
            value = default or key

        if kwargs:
            try:
                value = value.format(**kwargs)
            except KeyError as e:
                logger.warning(f"Missing parameter {e} for translation key: {key}")
                try:
                    for k, v in kwargs.items():
                        placeholder = f"{{{k}}}"
                        if placeholder in value:
                            value = value.replace(placeholder, str(v))
                except Exception:
                    pass

        return value

    def _get_nested(self, data: Dict[str, Any], key: str) -> Optional[str]:
        if not data:
            return None

        parts = key.split('.')
        current = data

        for part in parts:
            if not isinstance(current, dict):
                return None
            if part not in current:
                return None
            current = current[part]

        return current if isinstance(current, str) else None

    def reload_locale(self, lang: str) -> bool:
        if lang not in self.supported_languages:
            return False

        self._load_locale(lang)
        return True

    def get_all_keys(self, lang: str) -> Dict[str, str]:
        return self._flat_translations.get(lang, {}).copy()

    def validate_locale(self, lang: str) -> Dict[str, str]:
        if lang == self.default_language or not self.has_language(lang):
            return {}

        ref_keys = self.get_all_keys(self.default_language)
        current_keys = self.get_all_keys(lang)

        missing_keys = {}
        for key in ref_keys:
            if key not in current_keys:
                missing_keys[key] = ref_keys[key]

        return missing_keys

    def has_language(self, lang: str) -> bool:
        return lang in self._translations and bool(self._translations[lang])

    def get_language_name(self, lang: str, target_lang: Optional[str] = None) -> str:
        if target_lang is None:
            target_lang = lang

        name = self.get("language_name", target_lang, default=lang)

        if name == "language_name" or name == lang:
            name = self.get("language_name", lang, default=lang)

        return name

    def get_available_languages(self) -> Dict[str, str]:
        result = {}
        for lang in self.supported_languages:
            if self.has_language(lang):
                result[lang] = self.get_language_name(lang)
        return result

    def get_translation_stats(self) -> Dict[str, Any]:
        stats = {}
        for lang in self.supported_languages:
            if self.has_language(lang):
                keys_count = len(self._flat_translations.get(lang, {}))
                stats[lang] = {
                    "keys": keys_count,
                    "loaded": True,
                    "has_errors": keys_count == 0
                }
            else:
                stats[lang] = {"loaded": False, "keys": 0, "has_errors": True}

        return stats


i18n_loader = I18nLoader()