import asyncio
import json
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
            raise ConfigurationError(
                "GROQ_API_KEY is required for Groq provider."
            )

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
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    temperature=self._temperature,
                ),
                timeout=self._timeout,
            )

            text = (
                response.choices[0].message.content
                if response.choices
                else None
            )

            if not text:
                raise GeminiServiceError(
                    "Groq returned an empty response."
                )

            return text.strip()

        except asyncio.TimeoutError as exc:
            logger.exception("Groq request timed out.")
            raise GeminiServiceError(
                "Groq request timed out."
            ) from exc

        except GeminiServiceError:
            raise

        except Exception as exc:
            logger.exception("Groq API request failed.")
            raise GeminiServiceError(
                "Groq API request failed."
            ) from exc

    async def generate_with_tools(
        self,
        prompt: str,
        tools: list,
    ) -> str:
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        groq_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_research_papers",
            "description": (
                "Search the indexed research paper collection "
                "for information relevant to a query."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The research question or topic "
                            "to search for."
                        ),
                    }
                },
                "required": ["query"],
            },
        },
    }
]

        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    self._client.chat.completions.create,
                    model=self._model,
                    messages=messages,
                    tools=groq_tools,
                    tool_choice="auto",
                    temperature=self._temperature,
                ),
                timeout=self._timeout,
            )

            response_message = response.choices[0].message

            if not response_message.tool_calls:
                if not response_message.content:
                    raise GeminiServiceError(
                        "Groq returned an empty response."
                    )

                return response_message.content.strip()

            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(
                    tool_call.function.arguments
                )

                if function_name == "search_research_papers":
                    from rag.research_paper_tool import (
                        search_research_papers
                    )

                    function_response = search_research_papers(
                        query=function_args["query"]
                    )

                else:
                    raise GeminiServiceError(
                        f"Unknown tool requested: {function_name}"
                    )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(function_response),
                    }
                )

            final_response = await asyncio.wait_for(
                asyncio.to_thread(
                    self._client.chat.completions.create,
                    model=self._model,
                    messages=messages,
                    temperature=self._temperature,
                ),
                timeout=self._timeout,
            )

            final_message = final_response.choices[0].message

            if not final_message.content:
                raise GeminiServiceError(
                    "Groq returned an empty final response."
                )

            return final_message.content.strip()

        except asyncio.TimeoutError as exc:
            logger.exception(
                "Groq tool-enabled request timed out."
            )
            raise GeminiServiceError(
                "Groq tool-enabled request timed out."
            ) from exc

        except GeminiServiceError:
            raise

        except Exception as exc:
            logger.exception(
                "Groq tool-enabled API request failed."
            )
            raise GeminiServiceError(
                "Groq tool-enabled API request failed."
            ) from exc