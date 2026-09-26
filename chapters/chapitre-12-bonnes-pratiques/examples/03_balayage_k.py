"""Balayage de k et détection simple du coude de rappel."""

from __future__ import annotations

from collections.abc import Sequence
from itertools import pairwise


def balayer_k(
    questions: Sequence[dict[str, object]],
    retriever,
    valeurs_k: Sequence[int] = (1, 3, 5, 10, 15, 20),
) -> list[dict[str, float | int]]:
    if not questions:
        raise ValueError("questions ne peut pas être vide")
    values = sorted(set(valeurs_k))
    if not values or any(k <= 0 for k in values):
        raise ValueError("Les valeurs de k doivent être strictement positives")

    results = []
    for k in values:
        recalls = []
        for case in questions:
            expected = set(case["passages_attendus"])
            if not expected:
                raise ValueError("passages_attendus ne peut pas être vide")
            retrieved = retriever.chercher(str(case["texte"]), k=k)
            retrieved_ids = {passage.id for passage in retrieved}
            recalls.append(len(retrieved_ids & expected) / len(expected))
        results.append({"k": k, "rappel": round(sum(recalls) / len(recalls), 3)})
    return results


def choisir_coude(
    resultats: Sequence[dict[str, float | int]],
    *,
    gain_minimal: float = 0.02,
) -> int:
    """Retourne le premier k dont le gain suivant devient faible."""

    if not resultats:
        raise ValueError("resultats ne peut pas être vide")
    if gain_minimal < 0:
        raise ValueError("gain_minimal ne peut pas être négatif")
    for current, following in pairwise(resultats):
        gain = float(following["rappel"]) - float(current["rappel"])
        if gain < gain_minimal:
            return int(current["k"])
    return int(resultats[-1]["k"])


if __name__ == "__main__":
    sample = [
        {"k": 1, "rappel": 0.41},
        {"k": 3, "rappel": 0.68},
        {"k": 5, "rappel": 0.77},
        {"k": 10, "rappel": 0.78},
    ]
    print("Coude suggéré : k =", choisir_coude(sample, gain_minimal=0.02))
