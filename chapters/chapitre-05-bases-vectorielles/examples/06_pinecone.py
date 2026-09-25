"""Créer un index Pinecone serverless et insérer un lot de vecteurs."""

from __future__ import annotations

import os
from typing import Any


def connecter_pinecone(api_key: str | None = None):
    from pinecone import Pinecone

    cle = api_key or os.getenv("PINECONE_API_KEY")
    if not cle:
        raise RuntimeError("Définissez PINECONE_API_KEY pour utiliser Pinecone.")
    return Pinecone(api_key=cle)


def preparer_index(
    pc: Any,
    nom: str = "rag-production",
    dimension: int = 1536,
    cloud: str = "aws",
    region: str = "eu-west-1",
):
    from pinecone import ServerlessSpec

    if nom not in pc.list_indexes().names():
        pc.create_index(
            name=nom,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud=cloud, region=region),
        )
    return pc.Index(nom)


def inserer_passage(index, vecteur: list[float], namespace: str = "finance") -> None:
    index.upsert(
        vectors=[
            {
                "id": "chunk_001",
                "values": vecteur,
                "metadata": {
                    "source": "rapport_annuel_2024.pdf",
                    "page": 15,
                    "departement": "finance",
                    "texte": "Le chiffre d'affaires annuel atteint...",
                },
            }
        ],
        namespace=namespace,
    )


if __name__ == "__main__":
    if not os.getenv("PINECONE_API_KEY"):
        print("Exemple prêt : définissez PINECONE_API_KEY pour créer l'index distant.")
    else:
        pinecone = connecter_pinecone()
        print(preparer_index(pinecone))
