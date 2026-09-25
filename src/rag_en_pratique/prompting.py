"""Utilitaires pédagogiques partagés par les exemples de prompt engineering."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Passage:
    page_content: str
    metadata: dict[str, Any] = field(default_factory=dict)


def formater_simple(passages: list[Passage]) -> str:
    blocs = []
    for numero, passage in enumerate(passages, start=1):
        source = passage.metadata.get("source", "document inconnu")
        page = passage.metadata.get("page", "?")
        blocs.append(f"[doc_{numero}] {source}, page {page}\n{passage.page_content}")
    return "\n\n---\n\n".join(blocs)


def generer(
    instructions: str,
    entree: str | list[dict[str, str]],
    *,
    client=None,
    model: str | None = None,
) -> str:
    """Appelle Responses avec un client injectable pour les tests."""
    if client is None:
        from openai import OpenAI

        client = OpenAI()
    model = model or os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Définissez OPENAI_MODEL.")
    response = client.responses.create(model=model, instructions=instructions, input=entree)
    return response.output_text.strip()


def openai_configure() -> bool:
    return bool(os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_MODEL"))
