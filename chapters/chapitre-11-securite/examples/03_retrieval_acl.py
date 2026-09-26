"""Contrôle d'accès appliqué avant le calcul de similarité."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from qdrant_client.models import FieldCondition, Filter, MatchAny


def construire_filtre_acl(user_roles: Sequence[str]) -> Filter:
    roles = sorted({role.strip() for role in user_roles if role.strip()})
    if not roles:
        raise PermissionError("Aucun rôle authentifié : retrieval refusé")
    return Filter(
        must=[FieldCondition(key="allowed_roles", match=MatchAny(any=roles))]
    )


def retrieve_with_access_control(
    query: str,
    user_roles: Sequence[str],
    vector_store,
    *,
    k: int = 5,
):
    """Envoie le filtre ACL à la base, avant de sélectionner les voisins."""

    if k <= 0:
        raise ValueError("k doit être strictement positif")
    return vector_store.similarity_search(
        query,
        k=k,
        filter=construire_filtre_acl(user_roles),
    )


def filtrer_documents_autorises(
    documents: Iterable[dict[str, object]],
    user_roles: Sequence[str],
) -> list[dict[str, object]]:
    """Version locale utilisée pour comprendre et tester la règle ACL."""

    roles = {role.strip() for role in user_roles if role.strip()}
    if not roles:
        return []
    return [
        document
        for document in documents
        if roles & set(document.get("allowed_roles", []))
    ]


if __name__ == "__main__":
    documents = [
        {"source": "public.md", "allowed_roles": ["employee"]},
        {"source": "salaires.md", "allowed_roles": ["rh_manager"]},
    ]
    print(filtrer_documents_autorises(documents, ["employee"]))
