"""API FastAPI minimale exposant le pipeline DocuRAG/OpenAI."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from rag_en_pratique.core import (
    Document,
    InMemoryVectorStore,
    RAGPipeline,
    split_documents,
)
from rag_en_pratique.openai_adapter import OpenAIEmbedder, OpenAIGenerator


class QueryRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=3, ge=1, le=10)


def build_pipeline() -> RAGPipeline:
    repository = Path(__file__).resolve().parents[3]
    documents = [
        Document(path.read_text(encoding="utf-8"), {"source": path.name})
        for path in sorted((repository / "data" / "sample").glob("*.md"))
        if path.name.lower() != "readme.md"
    ]
    store = InMemoryVectorStore(OpenAIEmbedder())
    store.add(split_documents(documents, chunk_size=80, overlap=15))
    return RAGPipeline(store, OpenAIGenerator())


app = FastAPI(title="DocuRAG", version="1.0.0")
pipeline: RAGPipeline | None = None


@app.on_event("startup")
def startup() -> None:
    global pipeline
    pipeline = build_pipeline()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok" if pipeline else "initializing"}


@app.post("/query")
def query(request: QueryRequest) -> dict[str, object]:
    if pipeline is None:
        raise RuntimeError("Le pipeline n'est pas initialisé")
    return pipeline.ask(request.question, top_k=request.top_k)
