"""Ingestion, chunking et indexation avec le fournisseur configuré."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from rag_en_pratique.core import Document, InMemoryVectorStore, split_documents
from rag_en_pratique.providers import create_embedder


def build_knowledge_base(documents: Sequence[Document]) -> InMemoryVectorStore:
    chunks = split_documents(documents, chunk_size=60, overlap=10)
    store = InMemoryVectorStore(create_embedder())
    store.add(chunks)
    return store


def main() -> None:
    repository = Path(__file__).resolve().parents[3]
    documents = [
        Document(path.read_text(encoding="utf-8"), {"source": path.name})
        for path in sorted((repository / "data" / "sample").glob("*.md"))
        if path.name.lower() != "readme.md"
    ]
    store = build_knowledge_base(documents)
    print(f"{len(store.documents)} chunks indexés")


if __name__ == "__main__":
    main()
