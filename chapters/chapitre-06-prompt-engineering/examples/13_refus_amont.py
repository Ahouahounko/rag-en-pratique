def repondre_avec_garde_fou(question: str, retriever, modele,
                            seuil_minimal: float = 0.35) -> dict:
    """Coupe court si aucun extrait n'est suffisamment pertinent.

    Le refus le plus fiable n'est pas celui que le modele decide :
    c'est celui que l'application impose avant de l'appeler.
    """
    passages = retriever.invoke(question)

    if not passages:
        return {"reponse": "Les documents fournis ne permettent pas "
                           "de repondre a cette question.",
                "confiance": "nulle", "sources": []}

    meilleur = max(p.metadata.get("score_reclassement", 0.0)
                   for p in passages)

    if meilleur < seuil_minimal:
        # On n'appelle meme pas le modele : economie et surete.
        return {"reponse": "Les documents fournis ne permettent pas "
                           "de repondre a cette question.",
                "confiance": "nulle", "sources": []}

    reponse = (PROMPT_REFUS | modele).invoke({
        "contexte": formater_simple(passages),
        "question": question,
    }).content

    confiance = ("elevee" if meilleur > 0.7
                 else "moyenne" if meilleur > 0.5
                 else "faible")

    return {"reponse": reponse, "confiance": confiance,
            "sources": passages}
