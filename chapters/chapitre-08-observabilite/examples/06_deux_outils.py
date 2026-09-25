"""Comparer campagne de mesure et test de non-régression."""

from __future__ import annotations

import statistics
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class CasDeTest:
    question: str
    reponse: str
    contexte: str


def evaluer_campagne(
    jeu: list[CasDeTest],
    metriques: dict[str, Callable[[CasDeTest], float]],
) -> dict[str, object]:
    details = []
    for cas in jeu:
        scores = {nom: mesure(cas) for nom, mesure in metriques.items()}
        details.append({"question": cas.question, **scores})
    moyennes = {
        nom: statistics.mean(ligne[nom] for ligne in details)
        for nom in metriques
        if details
    }
    return {"moyennes": moyennes, "details": details}


def verifier_non_regression(
    cas: CasDeTest,
    mesurer: Callable[[CasDeTest], float],
    seuil: float,
) -> float:
    score = mesurer(cas)
    if score < seuil:
        raise AssertionError(f"Score {score:.3f} inférieur au seuil {seuil:.3f}")
    return score


if __name__ == "__main__":
    exemple = CasDeTest("Durée ?", "24 mois [doc_1]", "Garantie 24 mois")
    mesure_locale = lambda cas: float("24 mois" in cas.reponse and "24 mois" in cas.contexte)
    print(evaluer_campagne([exemple], {"fidelite": mesure_locale}))
    print(verifier_non_regression(exemple, mesure_locale, seuil=0.8))
