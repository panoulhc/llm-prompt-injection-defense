from __future__ import annotations
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")


def _get_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Missing ANTHROPIC_API_KEY. Add it to your .env file."
        )

    return Anthropic(api_key=api_key)


def _extract_text(message) -> str:
    parts: list[str] = []

    for block in message.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)

    return "\n".join(parts).strip()


def call_claude(
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
    max_tokens: int = 1000,
    temperature: float = 0.0
) -> str:
    client = _get_client()

    message = client.messages.create(
        model=model or DEFAULT_MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return _extract_text(message)