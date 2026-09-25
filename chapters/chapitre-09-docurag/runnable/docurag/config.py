"""Configuration de DocuRAG lue depuis l'environnement."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_model: str | None = None
    chunk_size: int = 80
    chunk_overlap: int = 15
    top_k: int = 3

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            openai_model=os.getenv("OPENAI_MODEL") or None,
            chunk_size=int(os.getenv("DOCURAG_CHUNK_SIZE", "80")),
            chunk_overlap=int(os.getenv("DOCURAG_CHUNK_OVERLAP", "15")),
            top_k=int(os.getenv("DOCURAG_TOP_K", "3")),
        )
