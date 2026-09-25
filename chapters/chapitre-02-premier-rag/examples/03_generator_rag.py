"""Génère une réponse sourcée avec la Responses API d'OpenAI."""

from __future__ import annotations

from collections.abc import Sequence

from rag_en_pratique.core import Document, SearchResult
from rag_en_pratique.openai_adapter import OpenAIGenerator


def generate_answer(question: str, passages: Sequence[SearchResult]) -> str:
    return OpenAIGenerator().generate(question, passages)


def main() -> None:
    passages = [
        SearchResult(
            Document("Les retours sont acceptés sous 30 jours.", {"source": "retours.md"}),
            1.0,
        )
    ]
    print(
        generate_answer(
            "Sous combien de jours peut-on retourner un produit ?",
            passages,
        )
    )


if __name__ == "__main__":
    main()
