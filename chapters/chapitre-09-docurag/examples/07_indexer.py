"""Indexation vectorielle de DocuRAG avec le fournisseur configuré."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from rag_en_pratique.core import Document, InMemoryVectorStore
from rag_en_pratique.providers import create_embedder


class Indexeur:
    """Index local pédagogique ; remplaçable par Qdrant en production."""

    def __init__(self, provider: str | None = None, *, client=None) -> None:
        self.store = InMemoryVectorStore(create_embedder(provider, client=client))

    def indexer(self, chunks: Sequence[Document]) -> int:
        self.store.add(chunks)
        return len(chunks)


def main() -> None:
    chunks = [
        Document(path.read_text(encoding="utf-8"), {"source": path.name})
        for path in sorted(Path("data/sample").glob("*.md"))
        if path.name.lower() != "readme.md"
    ]
    print(f"{Indexeur().indexer(chunks)} document(s) indexé(s)")


if __name__ == "__main__":
    main()
