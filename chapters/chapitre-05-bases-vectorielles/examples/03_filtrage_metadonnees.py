from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter, FieldCondition, MatchValue, Range
)


def chercher_avec_filtres(client: QdrantClient,
                          collection: str,
                          vecteur_requete: list,
                          departement: str = None,
                          date_minimale: str = None,
                          k: int = 5) -> list:
    """Recherche semantique restreinte par metadonnees.

    Qdrant applique les conditions AVANT la traversee du graphe
    (pre-filtrage) : le sous-ensemble eligible est determine
    d'abord, puis les k plus proches y sont cherches. C'est ce
    qui evite les listes vides sur les filtres selectifs.
    """
    conditions = []

    if departement:
        conditions.append(FieldCondition(
            key="departement",
            match=MatchValue(value=departement),
        ))

    if date_minimale:
        conditions.append(FieldCondition(
            key="date",
            range=Range(gte=date_minimale),     # >= date_minimale
        ))

    return client.search(
        collection_name=collection,
        query_vector=vecteur_requete,
        query_filter=Filter(must=conditions) if conditions else None,
        limit=k,
        with_payload=True,
    )
