"""Pipeline d'ingestion DocuRAG utilisant le fournisseur configuré."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from rag_en_pratique.core import Document, InMemoryVectorStore, split_documents
from rag_en_pratique.providers import create_embedder


def ingerer(
    documents: Iterable[Document],
    *,
    provider: str | None = None,
    client=None,
) -> InMemoryVectorStore:
    chunks = split_documents(documents, chunk_size=80, overlap=15)
    store = InMemoryVectorStore(create_embedder(provider, client=client))
    store.add(chunks)
    return store


def main() -> None:
    documents = [
        Document(path.read_text(encoding="utf-8"), {"source": path.name})
        for path in sorted(Path("data/sample").glob("*.md"))
        if path.name.lower() != "readme.md"
    ]
    store = ingerer(documents)
    print(f"{len(store.documents)} chunk(s) indexé(s)")


if __name__ == "__main__":
    main()
