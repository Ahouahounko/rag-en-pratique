"""Configuration centralisée de DocuRAG."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    provider: str = "openai"
    generation_model: str | None = None
    chunk_size: int = 80
    chunk_overlap: int = 15
    initial_k: int = 10
    top_k: int = 3
    score_threshold: float = 0.15

    def __post_init__(self) -> None:
        if self.provider not in {"openai", "huggingface", "ollama"}:
            raise ValueError("RAG_PROVIDER invalide")
        if not 0 <= self.chunk_overlap < self.chunk_size:
            raise ValueError("DOCURAG_CHUNK_OVERLAP doit être inférieur à la taille")
        if self.initial_k < self.top_k:
            raise ValueError("DOCURAG_INITIAL_K doit être supérieur ou égal à DOCURAG_TOP_K")

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
            generation_model=os.getenv(model_variables.get(provider, "")) or None,
            chunk_size=int(os.getenv("DOCURAG_CHUNK_SIZE", "80")),
            chunk_overlap=int(os.getenv("DOCURAG_CHUNK_OVERLAP", "15")),
            initial_k=int(os.getenv("DOCURAG_INITIAL_K", "10")),
            top_k=int(os.getenv("DOCURAG_TOP_K", "3")),
            score_threshold=float(os.getenv("DOCURAG_SCORE_THRESHOLD", "0.15")),
        )


if __name__ == "__main__":
    settings = Settings.from_env()
    print(settings)
