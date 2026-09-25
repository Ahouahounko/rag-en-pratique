def selection_diversifiee(base_vectorielle, question: str,
                          k: int = 5,
                          fetch_k: int = 25,
                          lambda_mult: float = 0.6) -> list:
    """Retourne k documents pertinents ET complementaires.

    fetch_k : taille du vivier ou l'algorithme pioche.
              Trop petit, il n'a pas de quoi diversifier.
              Regle simple : 4 a 5 fois k.

    lambda_mult : le curseur.
              0.8 -> corpus propre, on veut surtout la pertinence
              0.6 -> valeur de depart raisonnable
              0.3 -> corpus tres redondant (versions, FAQ dupliquees)
    """
    return base_vectorielle.max_marginal_relevance_search(
        query=question,
        k=k,
        fetch_k=fetch_k,
        lambda_mult=lambda_mult,
    )
