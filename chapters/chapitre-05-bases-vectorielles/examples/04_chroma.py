"""Indexer et rechercher dans Chroma avec les embeddings OpenAI."""

from __future__ import annotations

import os
from pathlib import Path


def creer_collection(repertoire: str | Path = "./chroma_db"):
    """Crée une collection persistante ; OPENAI_API_KEY doit être définie."""
    import chromadb
    from chromadb.utils import embedding_functions

    cle = os.getenv("OPENAI_API_KEY")
    if not cle:
        raise RuntimeError("Définissez OPENAI_API_KEY pour cet exemple Chroma/OpenAI.")
    fonction = embedding_functions.OpenAIEmbeddingFunction(
        api_key=cle,
        model_name="text-embedding-3-small",
    )
    client = chromadb.PersistentClient(path=str(repertoire))
    return client.get_or_create_collection(
        name="base_documentaire",
        embedding_function=fonction,
        metadata={"hnsw:space": "cosine"},
    )


def indexer_et_chercher(collection) -> dict[str, object]:
    collection.upsert(
        documents=[
            "La garantie standard couvre 24 mois à compter de la livraison.",
            "Le remboursement peut être demandé sous 30 jours.",
        ],
        metadatas=[
            {"source": "cgv.pdf", "page": 8, "departement": "juridique"},
            {"source": "cgv.pdf", "page": 12, "departement": "juridique"},
        ],
        ids=["chunk_001", "chunk_002"],
    )
    return collection.query(
        query_texts=["politique de remboursement"],
        n_results=2,
        where={"departement": "juridique"},
    )


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Exemple prêt : définissez OPENAI_API_KEY pour l'exécuter.")
    else:
        print(indexer_et_chercher(creer_collection())["documents"])
