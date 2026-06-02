from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent Research Assistant"
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    llm_primary_provider: str = Field(default="gemini", alias="LLM_PRIMARY_PROVIDER")

    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.5-flash", alias="GEMINI_MODEL")
    gemini_temperature: float = Field(default=0.2, alias="GEMINI_TEMPERATURE")

    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_MODEL")
    groq_temperature: float = Field(default=0.2, alias="GROQ_TEMPERATURE")

    request_timeout_seconds: int = Field(default=60, alias="REQUEST_TIMEOUT_SECONDS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

