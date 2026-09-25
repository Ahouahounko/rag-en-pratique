"""Appliquer des filtres de métadonnées avant une recherche Qdrant."""

from __future__ import annotations

from typing import Any


def construire_filtre(departement: str | None = None, date_minimale: str | None = None):
    from qdrant_client.models import DatetimeRange, FieldCondition, Filter, MatchValue

    conditions = []
    if departement:
        conditions.append(FieldCondition(key="departement", match=MatchValue(value=departement)))
    if date_minimale:
        conditions.append(FieldCondition(key="date", range=DatetimeRange(gte=date_minimale)))
    return Filter(must=conditions) if conditions else None


def chercher_avec_filtres(
    client: Any,
    collection: str,
    vecteur_requete: list[float],
    departement: str | None = None,
    date_minimale: str | None = None,
    k: int = 5,
) -> list[Any]:
    """Effectue une recherche filtrée avec l'API universelle query_points."""
    resultat = client.query_points(
        collection_name=collection,
        query=vecteur_requete,
        query_filter=construire_filtre(departement, date_minimale),
        limit=k,
        with_payload=True,
    )
    return list(resultat.points)


if __name__ == "__main__":
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams

    qdrant = QdrantClient(":memory:")
    qdrant.create_collection("documents", vectors_config=VectorParams(size=3, distance=Distance.COSINE))
    qdrant.upsert(
        "documents",
        points=[
            PointStruct(id=1, vector=[1.0, 0.0, 0.0], payload={"departement": "juridique", "date": "2026-01-15", "texte": "Retour sous 30 jours"}),
            PointStruct(id=2, vector=[0.0, 1.0, 0.0], payload={"departement": "finance", "date": "2025-01-15", "texte": "Bilan annuel"}),
        ],
    )
    print([point.payload for point in chercher_avec_filtres(qdrant, "documents", [1, 0, 0], "juridique")])
