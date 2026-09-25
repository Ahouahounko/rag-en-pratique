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
    return split_documents(documents, chunk_size=chunk_size, overlap=overlap)
