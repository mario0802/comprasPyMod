from __future__ import annotations
from dotenv import load_dotenv
load_dotenv() 

import os
from functools import lru_cache


def _str_to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "proyecto")
    ENV: str = os.getenv("ENV", "development")  # development | staging | production
    DEBUG: bool = _str_to_bool(os.getenv("DEBUG", "true"))

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    # En development por defecto logs legibles en consola; en producción JSON.
    LOG_JSON: bool = _str_to_bool(
        os.getenv("LOG_JSON", "false" if ENV == "development" else "true")
    )

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-.env")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://usuario:password@localhost:5432/mi_db"
    )

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me-in-.env")
    JWT_ACCESS_TOKEN_EXPIRES_MIN: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MIN", "60")
    )

    API_TITLE = "Api Compras"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    @property
    def is_production(self) -> bool:
        return self.ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.ENV == "development"


@lru_cache
def _get_settings() -> Settings:
    return Settings()


settings = _get_settings()