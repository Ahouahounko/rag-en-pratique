"""Briques communes aux exemples RAG, indépendantes du fournisseur de modèles."""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Document:
    """Document textuel et métadonnées associées."""

    text: str
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class SearchResult:
    """Passage retrouvé avec son score de similarité."""

    document: Document
    score: float


class Embedder(Protocol):
    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


class Generator(Protocol):
    def generate(self, question: str, passages: Sequence[SearchResult]) -> str: ...


def split_document(
    document: Document,
    *,
    chunk_size: int = 80,
    overlap: int = 15,
) -> list[Document]:
    """Découpe un document par mots avec chevauchement."""

    if chunk_size <= 0:
        raise ValueError("chunk_size doit être strictement positif")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap doit être compris entre 0 et chunk_size - 1")
    words = document.text.split()
    if not words:
        return []
    step = chunk_size - overlap
    chunks: list[Document] = []
    for chunk_index, start in enumerate(range(0, len(words), step)):
        selected = words[start : start + chunk_size]
        if not selected:
            break
        metadata = dict(document.metadata)
        metadata.update({"chunk": chunk_index, "start_word": start})
        chunks.append(Document(text=" ".join(selected), metadata=metadata))
        if start + chunk_size >= len(words):
            break
    return chunks


def split_documents(
    documents: Iterable[Document],
    *,
    chunk_size: int = 80,
    overlap: int = 15,
) -> list[Document]:
    return [
        chunk
        for document in documents
        for chunk in split_document(document, chunk_size=chunk_size, overlap=overlap)
    ]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Les vecteurs doivent avoir la même dimension")
    dot_product = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot_product / (left_norm * right_norm)


class InMemoryVectorStore:
    """Index vectoriel minimal pour les notebooks et les tests."""

    def __init__(self, embedder: Embedder) -> None:
        self.embedder = embedder
        self.documents: list[Document] = []
        self.vectors: list[list[float]] = []

    def add(self, documents: Sequence[Document]) -> None:
        self.documents.extend(documents)
        self.vectors.extend(self.embedder.embed([document.text for document in documents]))

    def search(self, query: str, *, top_k: int = 3) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k doit être strictement positif")
        query_vector = self.embedder.embed([query])[0]
        ranked = sorted(
            (
                SearchResult(document=document, score=cosine_similarity(query_vector, vector))
                for document, vector in zip(self.documents, self.vectors, strict=True)
            ),
            key=lambda result: result.score,
            reverse=True,
        )
        return ranked[:top_k]


class RAGPipeline:
    """Pipeline RAG commun aux notebooks et au projet DocuRAG."""

    def __init__(self, store: InMemoryVectorStore, generator: Generator) -> None:
        self.store = store
        self.generator = generator

    def ask(self, question: str, *, top_k: int = 3) -> dict[str, object]:
        passages = self.store.search(question, top_k=top_k)
        return {
            "question": question,
            "answer": self.generator.generate(question, passages),
            "sources": [
                {
                    "score": round(passage.score, 4),
                    "text": passage.document.text,
                    "metadata": passage.document.metadata,
                }
                for passage in passages
            ],
        }
