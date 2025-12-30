import os
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class BotSettings(BaseModel):
    token: str = ""
    admin_ids: List[int] = []


class DatabaseSettings(BaseModel):
    host: str = "postgres"
    port: int = 5432
    database: str = "gym_delivery"
    user: str = "postgres"
    password: str = "postgres"
    echo: bool = False
    pool_size: int = 20
    max_overflow: int = 10

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class LocalizationSettings(BaseModel):
    default_language: str = "ru"
    supported_languages: List[str] = ["ru", "uz", "en"]
    fallback_language: str = "en"
    locales_path: str = "locales"


class Settings:
    def __init__(self):
        self.bot = BotSettings(
            token=os.getenv("BOT_TOKEN", ""),
            admin_ids=self._parse_admin_ids(os.getenv("ADMIN_IDS", ""))
        )

        self.database = DatabaseSettings(
            host=os.getenv("POSTGRES_HOST", "postgres"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "gym_delivery"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            echo=os.getenv("POSTGRES_ECHO", "false").lower() == "true"
        )

        self.localization = LocalizationSettings(
            default_language=os.getenv("I18N_DEFAULT_LANGUAGE", "ru"),
            supported_languages=os.getenv("I18N_SUPPORTED_LANGUAGES", "ru,uz,en").split(","),
            fallback_language=os.getenv("I18N_FALLBACK_LANGUAGE", "en"),
            locales_path=os.getenv("I18N_LOCALES_PATH", "locales")
        )

        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.timezone = os.getenv("TIMEZONE", "Asia/Tashkent")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

    def _parse_admin_ids(self, admin_ids_str: str) -> List[int]:
        if not admin_ids_str or admin_ids_str == "bot_token_qoyiladi":
            return []

        try:
            return [int(x.strip()) for x in admin_ids_str.split(",") if x.strip()]
        except ValueError:
            return []

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.database.user}:{self.database.password}@{self.database.host}:{self.database.port}/{self.database.database}"


settings = Settings()