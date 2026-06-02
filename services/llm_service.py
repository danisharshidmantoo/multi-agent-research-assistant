import logging

from services.config import get_settings
from services.exceptions import ConfigurationError, GeminiServiceError
from services.gemini_service import GeminiService
from services.groq_service import GroqService


logger = logging.getLogger(__name__)


class LLMService:
    """
    Unified LLM interface used by agents.
    Tries the configured primary provider first, then falls back to the other provider.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self._primary = settings.llm_primary_provider.lower().strip()

        self._gemini = GeminiService() if settings.gemini_api_key else None
        self._groq = GroqService() if settings.groq_api_key else None

        if self._gemini is None and self._groq is None:
            raise ConfigurationError(
                "At least one provider key is required (GEMINI_API_KEY or GROQ_API_KEY)."
            )

    async def generate(self, prompt: str) -> str:
        providers = self._provider_order()
        last_error: Exception | None = None

        for name in providers:
            svc = self._gemini if name == "gemini" else self._groq
            if svc is None:
                continue
            try:
                return await svc.generate(prompt)
            except Exception as exc:
                last_error = exc
                logger.warning("Provider '%s' failed. Trying next provider.", name)

        raise GeminiServiceError("All configured LLM providers failed.") from last_error

    def _provider_order(self) -> list[str]:
        if self._primary == "groq":
            return ["groq", "gemini"]
        return ["gemini", "groq"]

