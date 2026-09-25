"""API FastAPI minimale exposant le pipeline DocuRAG multi-fournisseur."""

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
from rag_en_pratique.providers import create_provider


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
    provider = create_provider()
    store = InMemoryVectorStore(provider.embedder)
    store.add(split_documents(documents, chunk_size=80, overlap=15))
    return RAGPipeline(store, provider.generator)


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
