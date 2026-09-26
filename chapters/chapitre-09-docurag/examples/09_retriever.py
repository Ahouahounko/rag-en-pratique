"""Retrieval hybride : classement dense, lexical puis fusion RRF."""

from __future__ import annotations

from collections.abc import Sequence

from rag_en_pratique.core import Document, InMemoryVectorStore, SearchResult
from rag_en_pratique.providers import create_embedder


def fusion_rrf(
    rankings: Sequence[Sequence[SearchResult]],
    *,
    k: int = 60,
) -> list[SearchResult]:
    scores: dict[int, float] = {}
    documents: dict[int, Document] = {}
    for ranking in rankings:
        for rank, result in enumerate(ranking, start=1):
            key = id(result.document)
            documents[key] = result.document
            scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank)
    return sorted(
        (SearchResult(documents[key], score) for key, score in scores.items()),
        key=lambda result: result.score,
        reverse=True,
    )


def retrieve(
    store: InMemoryVectorStore,
    question: str,
    *,
    top_k: int = 5,
) -> list[SearchResult]:
    dense = store.search(question, top_k=top_k * 2)
    query_words = set(question.lower().split())
    lexical = sorted(
        (
            SearchResult(document, len(query_words & set(document.text.lower().split())))
            for document in store.documents
        ),
        key=lambda result: result.score,
        reverse=True,
    )
    return fusion_rrf([dense, lexical])[:top_k]


def main() -> None:
    store = InMemoryVectorStore(create_embedder())
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
