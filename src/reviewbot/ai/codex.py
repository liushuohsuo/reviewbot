"""OpenAI Codex integration layer."""

import json
from typing import Any

from openai import AsyncOpenAI

from reviewbot.config import settings


class CodexClient:
    """Async client for OpenAI Codex API."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            organization=settings.openai_org_id,
        )

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "gpt-5",
        max_tokens: int | None = None,
        temperature: float = 0.3,
    ) -> str:
        """Send a chat completion request and return the response text."""
        response = await self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens or settings.max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content or ""

    async def chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "gpt-5",
    ) -> dict[str, Any]:
        """Send a chat completion and parse the response as JSON."""
        text = await self.chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
            temperature=0.1,
        )
        # Handle code-fenced JSON
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        return json.loads(text)


# Singleton
codex = CodexClient()