"""Schémas d'entrée et de sortie de DocuRAG."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class QuestionRequest:
    question: str
    top_k: int = 3


@dataclass(frozen=True)
class SourceResponse:
    source: str
    text: str
    score: float


@dataclass(frozen=True)
class AnswerResponse:
    answer: str
    sources: list[SourceResponse] = field(default_factory=list)
