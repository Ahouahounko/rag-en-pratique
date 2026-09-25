"""Orchestration ingestion, retrieval et génération de DocuRAG."""

from __future__ import annotations

from pathlib import Path

from rag_en_pratique.core import (
    InMemoryVectorStore,
    RAGPipeline,
    split_documents,
)
from rag_en_pratique.providers import create_provider

from .config import Settings
from .loaders import load_directory


class DocuRAG:
    def __init__(self, settings: Settings | None = None, *, client=None) -> None:
        self.settings = settings or Settings.from_env()
        generation_model = self.settings.generation_model or self.settings.openai_model
        provider = create_provider(
            self.settings.provider,
            generation_model=generation_model,
            client=client,
        )
        self.store = InMemoryVectorStore(provider.embedder)
        self.pipeline = RAGPipeline(
            self.store,
            provider.generator,
        )

    def ingest(self, directory: Path) -> int:
        documents = load_directory(directory)
        chunks = split_documents(
            documents,
            chunk_size=self.settings.chunk_size,
            overlap=self.settings.chunk_overlap,
        )
        self.store.add(chunks)
        return len(chunks)

    def ask(self, question: str) -> dict[str, object]:
        return self.pipeline.ask(question, top_k=self.settings.top_k)
