"""Configuration de DocuRAG lue depuis l'environnement."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    provider: str = "openai"
    openai_model: str | None = None
    generation_model: str | None = None
    chunk_size: int = 80
    chunk_overlap: int = 15
    retrieval_initial_k: int = 10
    top_k: int = 3
    retrieval_score_threshold: float = 0.15
    use_hybrid_search: bool = True
    app_name: str = "DocuRAG"
    app_version: str = "1.0.0"

    def __post_init__(self) -> None:
        if self.provider not in {"openai", "huggingface", "ollama"}:
            raise ValueError("provider doit être openai, huggingface ou ollama")
        if self.chunk_size <= 0:
            raise ValueError("chunk_size doit être strictement positif")
        if not 0 <= self.chunk_overlap < self.chunk_size:
            raise ValueError("chunk_overlap doit être compris entre 0 et chunk_size - 1")
        if self.retrieval_initial_k < self.top_k or self.top_k <= 0:
            raise ValueError("retrieval_initial_k doit être supérieur ou égal à top_k")

    @classmethod
    def from_env(cls) -> Settings:
        provider = os.getenv("RAG_PROVIDER", "openai").lower()
        model_variables = {
            "openai": "OPENAI_MODEL",
            "huggingface": "HF_GENERATION_MODEL",
            "ollama": "OLLAMA_MODEL",
        }
        return cls(
            provider=provider,
            openai_model=os.getenv("OPENAI_MODEL") or None,
            generation_model=os.getenv(model_variables.get(provider, "")) or None,
            chunk_size=int(os.getenv("DOCURAG_CHUNK_SIZE", "80")),
            chunk_overlap=int(os.getenv("DOCURAG_CHUNK_OVERLAP", "15")),
            retrieval_initial_k=int(os.getenv("DOCURAG_INITIAL_K", "10")),
            top_k=int(os.getenv("DOCURAG_TOP_K", "3")),
            retrieval_score_threshold=float(os.getenv("DOCURAG_SCORE_THRESHOLD", "0.15")),
            use_hybrid_search=os.getenv("DOCURAG_HYBRID", "true").lower()
            in {"1", "true", "yes"},
        )
