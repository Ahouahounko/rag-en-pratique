"""Génère une réponse sourcée avec le fournisseur configuré."""

from __future__ import annotations

from collections.abc import Sequence

from rag_en_pratique.core import Document, SearchResult
from rag_en_pratique.providers import create_generator


def generate_answer(question: str, passages: Sequence[SearchResult]) -> str:
    return create_generator().generate(question, passages)


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
