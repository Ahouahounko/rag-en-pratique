"""Indexation vectorielle de DocuRAG avec le fournisseur configuré."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from rag_en_pratique.core import Document, InMemoryVectorStore
from rag_en_pratique.providers import create_embedder


class Indexeur:
    def __init__(self) -> None:
        self.store = InMemoryVectorStore(create_embedder())

    def indexer(self, chunks: Sequence[Document]) -> int:
        self.store.add(chunks)
        return len(chunks)


def main() -> None:
    repository = Path(__file__).resolve().parents[3]
    chunks = [
        Document(path.read_text(encoding="utf-8"), {"source": path.name})
        for path in sorted((repository / "data" / "sample").glob("*.md"))
        if path.name.lower() != "readme.md"
    ]
    print(f"{Indexeur().indexer(chunks)} document(s) indexé(s)")


if __name__ == "__main__":
    main()
