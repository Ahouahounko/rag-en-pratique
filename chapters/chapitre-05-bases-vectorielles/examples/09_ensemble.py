"""Fusionner un classement BM25 et un classement dense."""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Callable

from rank_bm25 import BM25Okapi


def tokeniser(texte: str) -> list[str]:
    return re.findall(r"\w+", texte.lower())


def fusion_rrf_ponderee(
    classements: list[list[str]],
    poids: list[float],
    constante: int = 60,
) -> list[str]:
    if len(classements) != len(poids):
        raise ValueError("Un poids est requis par classement")
    scores: dict[str, float] = defaultdict(float)
    for classement, poids_source in zip(classements, poids, strict=True):
        for rang, document in enumerate(classement, start=1):
            scores[document] += poids_source / (constante + rang)
    return sorted(scores, key=scores.get, reverse=True)


def construire_ensemble(
    documents: list[str],
    recherche_dense: Callable[[str, int], list[str]],
    poids: tuple[float, float] = (0.4, 0.6),
):
    bm25 = BM25Okapi([tokeniser(document) for document in documents])

    def rechercher(question: str, k: int = 5) -> list[str]:
        scores = bm25.get_scores(tokeniser(question))
        lexical = [documents[i] for i in sorted(range(len(documents)), key=scores.__getitem__, reverse=True)[:k]]
        dense = recherche_dense(question, k)
        return fusion_rrf_ponderee([lexical, dense], list(poids))[:k]

    return rechercher


if __name__ == "__main__":
    corpus = ["retour sous trente jours", "garantie de deux ans", "livraison en cinq jours"]
    dense_demo = lambda question, k: sorted(corpus, key=lambda texte: abs(len(texte) - len(question)))[:k]
    moteur = construire_ensemble(corpus, dense_demo)
    print(moteur("délai pour retourner un produit", k=2))
