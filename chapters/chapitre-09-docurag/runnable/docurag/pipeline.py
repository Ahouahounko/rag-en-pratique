"""Orchestration ingestion, retrieval et génération de DocuRAG."""

from __future__ import annotations

from pathlib import Path

from rag_en_pratique.core import (
    ExtractiveGenerator,
    HashingEmbedder,
    InMemoryVectorStore,
    RAGPipeline,
    split_documents,
)

from .config import Settings
from .loaders import load_directory


class DocuRAG:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()
        if self.settings.use_openai:
            from rag_en_pratique.openai_adapter import OpenAIEmbedder, OpenAIGenerator

            embedder = OpenAIEmbedder()
            generator = OpenAIGenerator(self.settings.openai_model)
        else:
            embedder = HashingEmbedder()
            generator = ExtractiveGenerator()
        self.store = InMemoryVectorStore(embedder)
        self.pipeline = RAGPipeline(self.store, generator)

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
