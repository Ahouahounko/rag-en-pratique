"""Génération DocuRAG avec la Responses API d'OpenAI."""

from __future__ import annotations

from collections.abc import Sequence

from rag_en_pratique.core import Document, SearchResult
from rag_en_pratique.openai_adapter import OpenAIGenerator


class Generateur:
    def __init__(self, model: str | None = None) -> None:
        self.generator = OpenAIGenerator(model)

    def repondre(self, question: str, passages: Sequence[SearchResult]) -> str:
        return self.generator.generate(question, passages)


def main() -> None:
    passages = [
        SearchResult(
            Document("La livraison prend trois à cinq jours.", {"source": "livraison.md"}),
            1.0,
        )
    ]
    print(
        Generateur().repondre(
            "Quel est le délai de livraison ?",
            passages,
        )
    )


if __name__ == "__main__":
    main()
