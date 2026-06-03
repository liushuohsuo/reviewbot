"""Multi-model adapter layer for ReviewBot.

Supports: OpenAI Codex, Anthropic Claude, Google Gemini.
"""

from abc import ABC, abstractmethod
from typing import Any

from reviewbot.ai.codex import codex as codex_client
from reviewbot.config import settings


class AIBackend(ABC):
    """Abstract AI backend interface."""

    @abstractmethod
    async def chat(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        ...

    @abstractmethod
    async def chat_json(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> dict[str, Any]:
        ...


class CodexBackend(AIBackend):
    """OpenAI Codex backend — default and recommended."""

    async def chat(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        return await codex_client.chat(system_prompt, user_prompt, **kwargs)

    async def chat_json(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> dict[str, Any]:
        return await codex_client.chat_json(system_prompt, user_prompt, **kwargs)


class ClaudeBackend(AIBackend):
    """Anthropic Claude backend."""

    async def chat(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        # Placeholder — implement with anthropic SDK when needed
        raise NotImplementedError("Claude backend requires anthropic SDK")

    async def chat_json(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> dict[str, Any]:
        raise NotImplementedError("Claude backend requires anthropic SDK")


class GeminiBackend(AIBackend):
    """Google Gemini backend."""

    async def chat(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        # Placeholder — implement with google-generativeai SDK when needed
        raise NotImplementedError("Gemini backend requires google-generativeai SDK")

    async def chat_json(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> dict[str, Any]:
        raise NotImplementedError("Gemini backend requires google-generativeai SDK")


def get_backend(name: str | None = None) -> AIBackend:
    """Factory: return the configured AI backend."""
    backend_name = name or settings.default_model
    backends: dict[str, AIBackend] = {
        "codex": CodexBackend(),
        "claude": ClaudeBackend(),
        "gemini": GeminiBackend(),
    }
    if backend_name not in backends:
        raise ValueError(
            f"Unknown backend '{backend_name}'. Available: {list(backends)}"
        )
    return backends[backend_name]