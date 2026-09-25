from qdrant_client.models import Filter, FieldCondition, MatchAny

def retrieve_with_access_control(query: str,
                                 user_roles: list[str],
                                 vector_store,
                                 k: int = 5) -> list:
    """
    Retrieval avec filtrage des documents selon les roles utilisateur.
    Seuls les documents autorises pour les roles de l'utilisateur
    sont candidats au retrieval.

    Args:
        query : Question de l'utilisateur
        user_roles : Liste des roles de l'utilisateur
                     Ex: ["employee", "rh_manager"]
        vector_store : Base vectorielle (Qdrant)
        k : Nombre de chunks a recuperer

    Returns:
        Chunks filtres selon les droits d'acces
    """
    # Construction du filtre d'acces
    # Un chunk est accessible si au moins un des roles autorises
    # correspond a un des roles de l'utilisateur
    access_filter = Filter(
        must=[
            FieldCondition(
                key="allowed_roles",
                match=MatchAny(any=user_roles)
            )
        ]
    )

    # Le retrieval n'explore que les documents autorises
    results = vector_store.similarity_search(
        query,
        k=k,
        filter=access_filter
    )

    return results

# A l'ingestion, chaque chunk doit inclure les roles autorises :
# chunk.metadata["allowed_roles"] = ["employee", "rh_manager", "direction"]
# chunk.metadata["confidentiality"] = "confidentiel"
