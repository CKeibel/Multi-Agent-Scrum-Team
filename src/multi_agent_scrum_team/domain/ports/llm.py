from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@runtime_checkable
class LLMPort(Protocol):
    """LLM Port/ Interface"""

    async def complete(
        self,
        messages: list[dict],
        response_format: type[T],
        tools: list[dict] | None = None,
        temperature: float = 0.0,
        **kwargs,
    ) -> T:
        ...
