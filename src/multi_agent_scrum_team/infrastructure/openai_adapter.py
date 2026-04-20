from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class OpenAIAdapter:
    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model
        self._client = AsyncOpenAI(api_key=self._api_key)

    async def complete(
        self,
        messages: list[dict],
        response_format: type[T],
        tools: list[dict] | None = None,
        temperature: float = 0.0,
        **kwargs,
    ) -> T:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            response_format=response_format,
            temperature=temperature,
            **({"tools": tools} if tools else {}),
            **kwargs,
        )
        message = response.choices[0].message

        if message.refusal:
            raise ValueError(f"Error during LLM call: {message.refusal}")

        return message.parsed
