"""Calculer les métriques de rang d'un retriever sans appel de modèle."""

from __future__ import annotations

import math


def evaluer_classement(
    recuperes: list[str],
    pertinents: set[str],
    k: int = 5,
) -> dict[str, float]:
    """Calcule Hit Rate, Precision@k, Recall@k, MRR et nDCG binaire."""
    if k <= 0:
        raise ValueError("k doit être strictement positif")
    tetes = recuperes[:k]
    trouves = [document for document in tetes if document in pertinents]
    hit = float(bool(trouves))
    precision = len(trouves) / k
    rappel = len(set(trouves)) / len(pertinents) if pertinents else 0.0
    mrr = next(
        (1.0 / rang for rang, document in enumerate(tetes, start=1) if document in pertinents),
        0.0,
    )
    dcg = sum(
        1.0 / math.log2(rang + 1)
        for rang, document in enumerate(tetes, start=1)
        if document in pertinents
    )
    ideal = sum(
        1.0 / math.log2(rang + 1)
        for rang in range(1, min(len(pertinents), k) + 1)
    )
    return {
        "hit_rate": hit,
        "precision_at_k": precision,
        "recall_at_k": rappel,
        "mrr": mrr,
        "ndcg": dcg / ideal if ideal else 0.0,
    }


if __name__ == "__main__":
    resultat = evaluer_classement(
        ["chunk_8", "chunk_2", "chunk_5", "chunk_1"],
        {"chunk_2", "chunk_1"},
        k=3,
    )
    print({nom: round(valeur, 3) for nom, valeur in resultat.items()})
