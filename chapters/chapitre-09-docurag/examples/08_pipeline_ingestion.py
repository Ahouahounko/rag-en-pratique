"""Pipeline d'ingestion DocuRAG utilisant OpenAI pour l'indexation."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from rag_en_pratique.core import Document, InMemoryVectorStore, split_documents
from rag_en_pratique.openai_adapter import OpenAIEmbedder


def ingerer(documents: Iterable[Document]) -> InMemoryVectorStore:
    chunks = split_documents(documents, chunk_size=80, overlap=15)
    store = InMemoryVectorStore(OpenAIEmbedder())
    store.add(chunks)
    return store


def main() -> None:
    repository = Path(__file__).resolve().parents[3]
    documents = [
        Document(path.read_text(encoding="utf-8"), {"source": path.name})
        for path in sorted((repository / "data" / "sample").glob("*.md"))
        if path.name.lower() != "readme.md"
    ]
    store = ingerer(documents)
    print(f"{len(store.documents)} chunk(s) indexé(s) avec OpenAI")


if __name__ == "__main__":
    main()
