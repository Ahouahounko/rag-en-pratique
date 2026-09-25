"""Configuration centralisée de DocuRAG."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_model: str
    embedding_model: str = "text-embedding-3-small"
    chunk_size: int = 80
    chunk_overlap: int = 15
    top_k: int = 3

    @classmethod
    def from_env(cls) -> Settings:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
        model = os.getenv("OPENAI_MODEL")
        if not model:
            raise RuntimeError("OPENAI_MODEL n'est pas configuré")
        return cls(
            openai_model=model,
            embedding_model=os.getenv(
                "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
            ),
            chunk_size=int(os.getenv("DOCURAG_CHUNK_SIZE", "80")),
            chunk_overlap=int(os.getenv("DOCURAG_CHUNK_OVERLAP", "15")),
            top_k=int(os.getenv("DOCURAG_TOP_K", "3")),
        )
