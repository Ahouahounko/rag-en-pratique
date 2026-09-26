"""Recherche hybride en mémoire : dense, lexicale puis fusion RRF."""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from rag_en_pratique.core import Document, InMemoryVectorStore, SearchResult

TOKEN_PATTERN = re.compile(r"\w+", flags=re.UNICODE)


@dataclass
class Passage:
    text: str
    source: str
    page: int = 0
    department: str = "general"
    dense_score: float = 0.0
    lexical_score: float = 0.0
    rerank_score: float = 0.0
    chunk_id: int = 0


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_PATTERN.findall(text) if len(token) > 2}


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[SearchResult]],
    *,
    k: int = 60,
) -> list[SearchResult]:
    """Fusionne des classements sans comparer des échelles incompatibles."""

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


class HybridRetriever:
    """Combine similarité vectorielle et recouvrement lexical."""

    def __init__(
        self,
        store: InMemoryVectorStore,
        *,
        initial_k: int = 10,
        final_k: int = 3,
        score_threshold: float = 0.15,
        hybrid: bool = True,
        reranker: Callable[[str, Sequence[Document]], Sequence[float]] | None = None,
    ) -> None:
        self.store = store
        self.initial_k = initial_k
        self.final_k = final_k
        self.score_threshold = score_threshold
        self.hybrid = hybrid
        self.reranker = reranker

    def search(
        self,
        question: str,
        *,
        filters: dict[str, object] | None = None,
    ) -> list[Passage]:
        dense = self.store.search(question, top_k=max(self.initial_k, len(self.store.documents)))
        dense = [result for result in dense if self._matches(result.document, filters)]
        dense = dense[: self.initial_k]

        if dense and dense[0].score < self.score_threshold:
            return []

        ranked = dense
        if self.hybrid:
            lexical = self._lexical(question, filters=filters)
            ranked = reciprocal_rank_fusion([dense, lexical])

        passages = [self._to_passage(item, dense) for item in ranked[: self.initial_k]]
        if self.reranker and len(passages) > 1:
            scores = self.reranker(question, [item.document for item in ranked])
            for passage, score in zip(passages, scores, strict=False):
                passage.rerank_score = float(score)
            passages.sort(key=lambda passage: passage.rerank_score, reverse=True)
        return passages[: self.final_k]

    def _lexical(
        self,
        question: str,
        *,
        filters: dict[str, object] | None,
    ) -> list[SearchResult]:
        query_tokens = _tokens(question)
        scored = []
        for document in self.store.documents:
            if not self._matches(document, filters):
                continue
            document_tokens = _tokens(document.text)
            union = query_tokens | document_tokens
            score = len(query_tokens & document_tokens) / len(union) if union else 0.0
            scored.append(SearchResult(document, score))
        return sorted(scored, key=lambda result: result.score, reverse=True)[: self.initial_k]

    @staticmethod
    def _matches(document: Document, filters: dict[str, object] | None) -> bool:
        return not filters or all(document.metadata.get(key) == value for key, value in filters.items())

    @staticmethod
    def _to_passage(result: SearchResult, dense: Sequence[SearchResult]) -> Passage:
        dense_scores = {id(item.document): item.score for item in dense}
        metadata = result.document.metadata
        return Passage(
            text=result.document.text,
            source=str(metadata.get("source", "document")),
            page=int(metadata.get("page", 0)),
            department=str(metadata.get("department", "general")),
            dense_score=dense_scores.get(id(result.document), 0.0),
            lexical_score=result.score,
            chunk_id=int(metadata.get("chunk", 0)),
        )
