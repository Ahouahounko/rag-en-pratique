"""Contrats Pydantic de l'API DocuRAG."""

from __future__ import annotations

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2_000)
    department: str | None = None


class SourceResponse(BaseModel):
    document: str
    page: int = 0
    department: str = "general"
    relevance: float


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceResponse] = Field(default_factory=list)
    confidence: str
    passage_count: int
    prompt_version: str
    duration_ms: int


class IngestionRequest(BaseModel):
    rebuild: bool = False
    path: str = "data/sample"


if __name__ == "__main__":
    request = QuestionRequest(question="Quel est le délai de livraison ?")
    print(request.model_dump())
