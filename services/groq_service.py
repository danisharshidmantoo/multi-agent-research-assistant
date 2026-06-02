import asyncio
import logging

from groq import Groq

from services.config import get_settings
from services.exceptions import ConfigurationError, GeminiServiceError


logger = logging.getLogger(__name__)


class GroqService:
    """Groq-backed text generation service used as provider fallback."""

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.groq_api_key:
            raise ConfigurationError("GROQ_API_KEY is required for Groq provider.")

        self._client = Groq(api_key=settings.groq_api_key)
        self._model = settings.groq_model
        self._temperature = settings.groq_temperature
        self._timeout = settings.request_timeout_seconds

    async def generate(self, prompt: str) -> str:
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    self._client.chat.completions.create,
                    model=self._model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self._temperature,
                ),
                timeout=self._timeout,
            )

            text = response.choices[0].message.content if response.choices else None
            if not text:
                raise GeminiServiceError("Groq returned an empty response.")
            return text.strip()
        except asyncio.TimeoutError as exc:
            logger.exception("Groq request timed out.")
            raise GeminiServiceError("Groq request timed out.") from exc
        except GeminiServiceError:
            raise
        except Exception as exc:
            logger.exception("Groq API request failed.")
            raise GeminiServiceError("Groq API request failed.") from exc

