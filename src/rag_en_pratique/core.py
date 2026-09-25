"""Briques RAG légères, déterministes et utilisables hors ligne."""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, field
from typing import Iterable, Protocol, Sequence


TOKEN_PATTERN = re.compile(r"[\wà-ÿ]+", re.IGNORECASE)
STOPWORDS = {
    "a",
    "au",
    "aux",
    "avec",
    "ce",
    "ces",
    "dans",
    "de",
    "des",
    "du",
    "elle",
    "en",
    "est",
    "et",
    "il",
    "la",
    "le",
    "les",
    "ou",
    "par",
    "pour",
    "que",
    "quel",
    "quelle",
    "qui",
    "se",
    "son",
    "sur",
    "un",
    "une",
}


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


def tokenize(text: str) -> list[str]:
    return [
        token.lower()
        for token in TOKEN_PATTERN.findall(text)
        if token.lower() not in STOPWORDS and len(token) > 1
    ]


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


class HashingEmbedder:
    """Embedding local sans téléchargement, destiné aux démonstrations."""

    def __init__(self, dimensions: int = 256) -> None:
        if dimensions <= 0:
            raise ValueError("dimensions doit être strictement positif")
        self.dimensions = dimensions

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in tokenize(text):
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            bucket = int.from_bytes(digest, "big") % self.dimensions
            vector[bucket] += 1.0
        norm = math.sqrt(sum(value * value for value in vector))
        return [value / norm for value in vector] if norm else vector


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Les vecteurs doivent avoir la même dimension")
    return sum(a * b for a, b in zip(left, right, strict=True))


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


class ExtractiveGenerator:
    """Générateur hors ligne qui cite les passages les plus pertinents."""

    def __init__(self, min_score: float = 0.12) -> None:
        self.min_score = min_score

    def generate(self, question: str, passages: Sequence[SearchResult]) -> str:
        del question
        best_score = passages[0].score if passages else 0.0
        useful = [
            passage
            for passage in passages
            if passage.score >= self.min_score and passage.score >= best_score * 0.6
        ]
        if not useful:
            return "Cette information n'est pas disponible dans les documents consultés."
        lines = ["Réponse extraite des documents :"]
        for index, passage in enumerate(useful, start=1):
            source = passage.document.metadata.get("source", "document")
            excerpt = passage.document.text.strip()
            lines.append(f"[{index}] {excerpt} (source : {source})")
        return "\n".join(lines)


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
