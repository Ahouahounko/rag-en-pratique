"""Réponse citée, abstention et traçabilité de DocuRAG."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from rag_en_pratique.core import Document, Generator, SearchResult

from .retrieval import Passage

ABSTENTION = "Cette information ne figure pas dans les documents consultés."
PROMPT_VERSION = "1.2"


@dataclass
class CitedAnswer:
    answer: str
    sources: list[dict[str, object]] = field(default_factory=list)
    confidence: str = "Bas"
    passage_count: int = 0
    prompt_version: str = PROMPT_VERSION


class CitedGenerator:
    def __init__(self, generator: Generator) -> None:
        self.generator = generator

    def answer(self, question: str, passages: Sequence[Passage]) -> CitedAnswer:
        if not passages:
            return CitedAnswer(answer=ABSTENTION)
        results = [
            SearchResult(
                Document(
                    passage.text,
                    {"source": passage.source, "page": passage.page},
                ),
                passage.rerank_score or passage.dense_score or passage.lexical_score,
            )
            for passage in passages
        ]
        return CitedAnswer(
            answer=self.generator.generate(question, results),
            sources=self._sources(passages),
            confidence=self._confidence(passages),
            passage_count=len(passages),
        )

    @staticmethod
    def format_context(passages: Sequence[Passage]) -> str:
        blocks = []
        for number, passage in enumerate(passages, start=1):
            page = f", page {passage.page}" if passage.page else ""
            blocks.append(f"[doc_{number}] {passage.source}{page}\n{passage.text}")
        return "\n\n---\n\n".join(blocks)

    @staticmethod
    def _confidence(passages: Sequence[Passage]) -> str:
        best = max(
            (item.rerank_score or item.dense_score or item.lexical_score for item in passages),
            default=0.0,
        )
        if best >= 0.7:
            return "Haut"
        return "Moyen" if best >= 0.4 else "Bas"

    @staticmethod
    def _sources(passages: Sequence[Passage]) -> list[dict[str, object]]:
        sources = []
        for passage in passages:
            score = passage.rerank_score or passage.dense_score or passage.lexical_score
            sources.append(
                {
                    "document": passage.source,
                    "page": passage.page,
                    "department": passage.department,
                    "relevance": round(score, 3),
                }
            )
        return sources
