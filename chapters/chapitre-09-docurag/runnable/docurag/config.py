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
    top_k: int = 3

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
            top_k=int(os.getenv("DOCURAG_TOP_K", "3")),
        )
