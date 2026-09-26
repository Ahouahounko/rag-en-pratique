"""Orchestration ingestion, retrieval et génération de DocuRAG."""

from __future__ import annotations

from pathlib import Path

from rag_en_pratique.core import (
    Document,
    InMemoryVectorStore,
    split_documents,
)
from rag_en_pratique.providers import create_provider

from .config import Settings
from .generation import CitedGenerator
from .loaders import load_directory
from .retrieval import HybridRetriever


class DocuRAG:
    def __init__(self, settings: Settings | None = None, *, client=None) -> None:
        self.settings = settings or Settings.from_env()
        generation_model = self.settings.generation_model or self.settings.openai_model
        provider = create_provider(
            self.settings.provider,
            generation_model=generation_model,
            client=client,
        )
        self.provider = provider
        self.store = InMemoryVectorStore(provider.embedder)
        self.generator = CitedGenerator(provider.generator)
        self.retriever = self._build_retriever()
        self._documents: dict[str, list[Document]] = {}

    def _build_retriever(self) -> HybridRetriever:
        return HybridRetriever(
            self.store,
            initial_k=self.settings.retrieval_initial_k,
            final_k=self.settings.top_k,
            score_threshold=self.settings.retrieval_score_threshold,
            hybrid=self.settings.use_hybrid_search,
        )

    def ingest(self, directory: Path, *, rebuild: bool = False) -> int:
        documents = load_directory(directory)
        incoming = {
            str(document.metadata["source_path"]): str(document.metadata["fingerprint"])
            for document in documents
        }
        current = {
            source: str(items[0].metadata["fingerprint"])
            for source, items in self._documents.items()
            if items
        }
        if not rebuild and incoming == current:
            return 0

        self._documents = {}
        for document in documents:
            source = str(document.metadata["source_path"])
            self._documents.setdefault(source, []).append(document)
        chunks = split_documents(
            [item for items in self._documents.values() for item in items],
            chunk_size=self.settings.chunk_size,
            overlap=self.settings.chunk_overlap,
        )
        self.store = InMemoryVectorStore(self.provider.embedder)
        self.store.add(chunks)
        self.retriever = self._build_retriever()
        return len(chunks)

    def ask(
        self,
        question: str,
        *,
        filters: dict[str, object] | None = None,
    ) -> dict[str, object]:
        passages = self.retriever.search(question, filters=filters)
        response = self.generator.answer(question, passages)
        return {
            "question": question,
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
            "passage_count": response.passage_count,
            "prompt_version": response.prompt_version,
        }
