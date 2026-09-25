"""Adaptateurs de modèles interchangeables pour les exemples RAG."""

from __future__ import annotations

import json
import os
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from .core import Embedder, Generator, SearchResult
from .openai_adapter import OpenAIEmbedder, OpenAIGenerator

SUPPORTED_PROVIDERS = ("openai", "huggingface", "ollama")


def _provider_name(provider: str | None = None) -> str:
    selected = (provider or os.getenv("RAG_PROVIDER", "openai")).strip().lower()
    if selected not in SUPPORTED_PROVIDERS:
        choices = ", ".join(SUPPORTED_PROVIDERS)
        raise ValueError(f"RAG_PROVIDER doit être l'un de : {choices}")
    return selected


def _grounded_prompt(question: str, passages: Sequence[SearchResult]) -> str:
    context = "\n\n".join(
        f"[Source {index}: {item.document.metadata.get('source', 'document')}]\n"
        f"{item.document.text}"
        for index, item in enumerate(passages, start=1)
    )
    return (
        "Réponds uniquement à partir des sources fournies. "
        "Si elles ne contiennent pas la réponse, dis-le clairement. "
        "Cite les sources entre crochets.\n\n"
        f"SOURCES\n{context}\n\nQUESTION\n{question}"
    )


class HuggingFaceEmbedder:
    """Embeddings locaux avec Sentence Transformers."""

    def __init__(self, model: str | None = None, *, encoder: Any = None) -> None:
        self.model = model or os.getenv(
            "HF_EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        if encoder is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError('Installez le fournisseur avec pip install -e ".[huggingface]"') from exc
            encoder = SentenceTransformer(self.model)
        self.encoder = encoder

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        vectors = self.encoder.encode(list(texts), normalize_embeddings=True)
        return [list(map(float, vector)) for vector in vectors]


class HuggingFaceGenerator:
    """Génération locale avec un pipeline Transformers."""

    def __init__(self, model: str | None = None, *, text_pipeline: Any = None) -> None:
        self.model = model or os.getenv("HF_GENERATION_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
        if text_pipeline is None:
            try:
                import torch
                from transformers import pipeline
            except ImportError as exc:
                raise RuntimeError('Installez le fournisseur avec pip install -e ".[huggingface]"') from exc
            device = 0 if torch.cuda.is_available() else -1
            text_pipeline = pipeline("text-generation", model=self.model, device=device)
        self.text_pipeline = text_pipeline

    def generate(self, question: str, passages: Sequence[SearchResult]) -> str:
        prompt = _grounded_prompt(question, passages)
        output = self.text_pipeline(
            [{"role": "user", "content": prompt}],
            max_new_tokens=int(os.getenv("HF_MAX_NEW_TOKENS", "256")),
            do_sample=False,
        )[0]["generated_text"]
        if isinstance(output, list):
            return str(output[-1]["content"])
        return str(output)[len(prompt) :].strip()


class OllamaEmbedder:
    """Embeddings servis par une instance Ollama locale."""

    def __init__(self, model: str | None = None, *, base_url: str | None = None) -> None:
        self.model = model or os.getenv("OLLAMA_EMBEDDING_MODEL", "embeddinggemma")
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        payload = _ollama_post(
            self.base_url,
            "/api/embed",
            {"model": self.model, "input": list(texts)},
        )
        return [[float(value) for value in vector] for vector in payload["embeddings"]]


class OllamaGenerator:
    """Génération servie par une instance Ollama locale."""

    def __init__(self, model: str | None = None, *, base_url: str | None = None) -> None:
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen3:0.6b")
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")

    def generate(self, question: str, passages: Sequence[SearchResult]) -> str:
        payload = _ollama_post(
            self.base_url,
            "/api/chat",
            {
                "model": self.model,
                "messages": [{"role": "user", "content": _grounded_prompt(question, passages)}],
                "stream": False,
            },
        )
        return str(payload["message"]["content"])


def _ollama_post(base_url: str, path: str, payload: dict[str, object]) -> dict[str, Any]:
    request = Request(
        f"{base_url}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except URLError as exc:
        raise RuntimeError(
            f"Ollama est inaccessible sur {base_url}. Démarrez Ollama et téléchargez les modèles."
        ) from exc


@dataclass(frozen=True)
class ProviderComponents:
    name: str
    embedder: Embedder
    generator: Generator


def create_embedder(provider: str | None = None, *, client: Any = None) -> Embedder:
    selected = _provider_name(provider)
    if selected == "openai":
        return OpenAIEmbedder(client=client)
    if selected == "huggingface":
        return HuggingFaceEmbedder()
    return OllamaEmbedder()


def create_generator(
    provider: str | None = None,
    *,
    model: str | None = None,
    client: Any = None,
) -> Generator:
    selected = _provider_name(provider)
    if selected == "openai":
        return OpenAIGenerator(model, client=client)
    if selected == "huggingface":
        return HuggingFaceGenerator(model)
    return OllamaGenerator(model)


def create_provider(
    provider: str | None = None,
    *,
    generation_model: str | None = None,
    client: Any = None,
) -> ProviderComponents:
    selected = _provider_name(provider)
    return ProviderComponents(
        name=selected,
        embedder=create_embedder(selected, client=client),
        generator=create_generator(selected, model=generation_model, client=client),
    )
