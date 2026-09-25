"""Adaptateurs OpenAI optionnels pour les exemples du livre.

Le module n'importe le SDK que lors de l'instanciation. Le mode hors ligne du
dépôt reste donc utilisable sans SDK ni clé API.
"""

from __future__ import annotations

import os
from collections.abc import Sequence

from .core import SearchResult


def _client():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError('Installez les dépendances avec pip install -e ".[openai]"') from exc
    return OpenAI()


class OpenAIEmbedder:
    """Embeddings via l'API OpenAI."""

    def __init__(self, model: str = "text-embedding-3-small") -> None:
        self.model = model
        self.client = _client()

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        response = self.client.embeddings.create(model=self.model, input=list(texts))
        return [item.embedding for item in response.data]


class OpenAIGenerator:
    """Génération fondée sur les passages retrouvés via Responses API."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL")
        if not self.model:
            raise RuntimeError("Configurez OPENAI_MODEL avant d'activer le mode OpenAI")
        self.client = _client()

    def generate(self, question: str, passages: Sequence[SearchResult]) -> str:
        context = "\n\n".join(
            f"[Source {index}: {item.document.metadata.get('source', 'document')}]\n"
            f"{item.document.text}"
            for index, item in enumerate(passages, start=1)
        )
        response = self.client.responses.create(
            model=self.model,
            instructions=(
                "Réponds uniquement à partir des sources fournies. "
                "Si elles ne contiennent pas la réponse, dis-le clairement. "
                "Cite les sources entre crochets."
            ),
            input=f"SOURCES\n{context}\n\nQUESTION\n{question}",
        )
        return response.output_text
