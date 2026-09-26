"""API FastAPI exposant ingestion, santé et interrogation DocuRAG."""

from __future__ import annotations

import sys
import time
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

RUNNABLE = Path("chapters/chapitre-09-docurag/runnable").resolve()
sys.path.insert(0, str(RUNNABLE))

from docurag import DocuRAG


class QueryRequest(BaseModel):
    question: str = Field(min_length=3)
    department: str | None = None


class IngestionRequest(BaseModel):
    rebuild: bool = False


def build_pipeline() -> DocuRAG:
    docurag = DocuRAG()
    docurag.ingest(Path("data/sample"), rebuild=True)
    return docurag


app = FastAPI(title="DocuRAG", version="1.0.0")
pipeline: DocuRAG | None = None


@app.on_event("startup")
def startup() -> None:
    global pipeline
    pipeline = build_pipeline()


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok" if pipeline else "initializing",
        "indexed_chunks": len(pipeline.store.documents) if pipeline else 0,
    }


@app.post("/ingest")
def ingest(request: IngestionRequest) -> dict[str, int]:
    if pipeline is None:
        raise RuntimeError("Le pipeline n'est pas initialisé")
    repository = Path.cwd()
    count = pipeline.ingest(repository / "data" / "sample", rebuild=request.rebuild)
    return {"indexed_chunks": count}


@app.post("/query")
def query(request: QueryRequest) -> dict[str, object]:
    if pipeline is None:
        raise RuntimeError("Le pipeline n'est pas initialisé")
    started = time.perf_counter()
    filters = {"department": request.department} if request.department else None
    result = pipeline.ask(request.question, filters=filters)
    result["duration_ms"] = round((time.perf_counter() - started) * 1_000)
    return result
