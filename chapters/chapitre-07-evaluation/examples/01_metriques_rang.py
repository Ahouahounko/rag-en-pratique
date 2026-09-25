import math


def evaluer_classement(recuperes: list[str],
                       pertinents: set[str],
                       k: int = 5) -> dict:
    """Mesure la qualite d'une liste ORDONNEE de passages.

    recuperes  : identifiants des passages, dans l'ordre du retriever
    pertinents : identifiants attendus (annotation de reference)

    Aucun appel de modele : ces metriques sont exactes,
    instantanees et parfaitement reproductibles.
    """
    tetes = recuperes[:k]
    trouves = [doc for doc in tetes if doc in pertinents]

    # Le systeme a-t-il une chance de repondre ?
    hit = 1.0 if trouves else 0.0

    precision = len(trouves) / k if k else 0.0
    rappel = len(trouves) / len(pertinents) if pertinents else 0.0

    # Rang du PREMIER passage pertinent : recompense la mise en tete
    mrr = 0.0
    for position, doc in enumerate(tetes, start=1):
        if doc in pertinents:
            mrr = 1.0 / position
            break

    # nDCG : le rang compte, avec un escompte logarithmique
    gain = sum(1.0 / math.log2(position + 1)
               for position, doc in enumerate(tetes, start=1)
               if doc in pertinents)
    ideal = sum(1.0 / math.log2(position + 1)
                for position in range(1, min(len(pertinents), k) + 1))
    ndcg = gain / ideal if ideal else 0.0

    return {"hit_rate": hit, "precision_at_k": precision,
            "recall_at_k": rappel, "mrr": mrr, "ndcg": ndcg}
