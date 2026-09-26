"""Découpage des documents avant l'indexation OpenAI."""

from __future__ import annotations

from collections.abc import Iterable

from rag_en_pratique.core import Document, split_documents


def decouper(
    documents: Iterable[Document],
    *,
    chunk_size: int = 80,
    overlap: int = 15,
) -> list[Document]:
    chunks = split_documents(documents, chunk_size=chunk_size, overlap=overlap)
    return [
        Document(
            chunk.text,
            {**chunk.metadata, "chunk_id": index, "chunk_size": len(chunk.text)},
        )
        for index, chunk in enumerate(chunks)
    ]


if __name__ == "__main__":
    sample = Document(" ".join(f"mot-{index}" for index in range(120)), {"source": "demo.txt"})
    for chunk in decouper([sample], chunk_size=40, overlap=8):
        print(chunk.metadata, chunk.text[:50])
