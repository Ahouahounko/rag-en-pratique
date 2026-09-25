"""Retrieval vectoriel utilisant les embeddings OpenAI."""

from __future__ import annotations

from rag_en_pratique.core import Document, InMemoryVectorStore, SearchResult
from rag_en_pratique.openai_adapter import OpenAIEmbedder


def retrieve(
    store: InMemoryVectorStore,
    question: str,
    *,
    top_k: int = 5,
) -> list[SearchResult]:
    return store.search(question, top_k=top_k)


def main() -> None:
    store = InMemoryVectorStore(OpenAIEmbedder())
    store.add(
        [
            Document("Les retours sont acceptés sous 30 jours.", {"source": "retours.md"}),
            Document("La livraison prend trois à cinq jours.", {"source": "livraison.md"}),
        ]
    )
    for result in retrieve(store, "Quel est le délai de retour ?", top_k=2):
        print(round(result.score, 4), result.document.metadata["source"])


if __name__ == "__main__":
    main()
