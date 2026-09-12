import asyncio
import logging

from click import prompt
import google.genai as genai
from google.genai import types
from openai import chat

from services.config import get_settings
from services.exceptions import ConfigurationError, GeminiServiceError


logger = logging.getLogger(__name__)


class GeminiService:
    """Wrapper for Gemini API communication."""

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.gemini_api_key:
            raise ConfigurationError("GEMINI_API_KEY is required.")
        #this creates gemini client object
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model
        self._fallback_models = ["gemini-2.0-flash", "gemini-1.5-flash-8b"]
        self._temperature = settings.gemini_temperature
        self._timeout = settings.request_timeout_seconds

    async def generate(self, prompt: str) -> str:
        """Generate text from Gemini model asynchronously."""
        model_candidates = [self._model] + [
            model for model in self._fallback_models if model != self._model
        ]

        try:
            for model_name in model_candidates:
                # Try each model up to 3 times to absorb transient provider-side spikes.
                for attempt in range(3):
                    try:
                        response = await asyncio.wait_for(
                            asyncio.to_thread(
                                self._client.models.generate_content,
                                model=model_name,
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    temperature=self._temperature,
                                ),
                            ),
                            timeout=self._timeout,
                        )

                        text = getattr(response, "text", None)
                        if not text:
                            raise GeminiServiceError("Gemini returned an empty response.")

                        if model_name != self._model:
                            logger.warning(
                                "Using fallback Gemini model '%s' after primary model issues.",
                                model_name,
                            )
                        return text.strip()
                    except Exception as exc:
                        error_text = str(exc).upper()
                        is_transient = "503" in error_text or "UNAVAILABLE" in error_text
                        is_last_attempt = attempt == 2
                        if is_transient and not is_last_attempt:
                            await asyncio.sleep(1.2 * (attempt + 1))
                            continue
                        if is_transient and is_last_attempt:
                            logger.warning(
                                "Transient Gemini error on model '%s'; trying next model.",
                                model_name,
                            )
                            break
                        raise
            raise GeminiServiceError(
                "Gemini service unavailable after retries and fallback attempts."
            )
        except asyncio.TimeoutError as exc:
            logger.exception("Gemini request timed out.")
            raise GeminiServiceError("Gemini request timed out.") from exc
        except GeminiServiceError:
            raise
        except Exception as exc:
            logger.exception("Gemini API request failed.")
            raise GeminiServiceError("Gemini API request failed.") from exc
    async def generate_with_tools(
        self,
        prompt: str,
        tools: list,
        ) -> str:
        """Generate text from Gemini with tool-calling support."""

        model_candidates = [self._model] + [
            model
            for model in self._fallback_models
            if model != self._model
        ]

        for model_name in model_candidates:
            for attempt in range(3):
                try:
                    chat = self._client.chats.create(
                    model=model_name,
                    config=types.GenerateContentConfig(
                    temperature=self._temperature,
                    tools=tools,
                    ),
)

                    response = await asyncio.wait_for(
                    asyncio.to_thread(
                    chat.send_message,
                     prompt,
                ),
                    timeout=self._timeout,
                        )
                    text = getattr(response, "text", None)

                    if not text:
                        raise GeminiServiceError(
                            "Gemini returned an empty response."
                        )

                    return text.strip()

                except Exception as exc:
                    error_text = str(exc).upper()

                    is_transient = (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                    )

                    is_last_attempt = attempt == 2

                    if is_transient and not is_last_attempt:
                        await asyncio.sleep(1.2 * (attempt + 1))
                        continue

                    if is_transient and is_last_attempt:
                        logger.warning(
                            "Transient Gemini error on model '%s'; "
                            "trying next model.",
                            model_name,
                        )
                        break

                    raise

        raise GeminiServiceError(
            "Gemini tool-enabled generation failed after retries "
            "and fallback attempts."
        )
