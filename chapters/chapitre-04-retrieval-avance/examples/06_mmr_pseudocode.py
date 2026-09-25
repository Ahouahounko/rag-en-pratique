"""Implémentation exécutable de Maximal Marginal Relevance (MMR)."""

import math
import re
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Candidat:
    texte: str
    source: str


def similarite(gauche: str, droite: str) -> float:
    a = Counter(re.findall(r"\w+", gauche.lower()))
    b = Counter(re.findall(r"\w+", droite.lower()))
    mots = set(a) | set(b)
    produit = sum(a[mot] * b[mot] for mot in mots)
    norme_a = math.sqrt(sum(valeur**2 for valeur in a.values()))
    norme_b = math.sqrt(sum(valeur**2 for valeur in b.values()))
    return produit / (norme_a * norme_b) if norme_a and norme_b else 0.0


def selection_mmr(
    candidats: list[Candidat],
    question: str,
    k: int,
    lambda_mult: float = 0.6,
) -> list[Candidat]:
    """Équilibre pertinence pour la question et diversité de la sélection."""

    if not 0 <= lambda_mult <= 1:
        raise ValueError("lambda_mult doit être compris entre 0 et 1")
    restants = list(candidats)
    selection: list[Candidat] = []
    while restants and len(selection) < k:
        def score(candidat: Candidat) -> float:
            pertinence = similarite(candidat.texte, question)
            redondance = max(
                (similarite(candidat.texte, retenu.texte) for retenu in selection),
                default=0.0,
            )
            return lambda_mult * pertinence - (1 - lambda_mult) * redondance

        meilleur = max(restants, key=score)
        selection.append(meilleur)
        restants.remove(meilleur)
    return selection


if __name__ == "__main__":
    documents = [
        Candidat("Retour produit possible pendant trente jours.", "retours-1.md"),
        Candidat("Le délai de retour produit est de trente jours.", "retours-2.md"),
        Candidat("Le remboursement arrive sous cinq jours.", "remboursement.md"),
    ]
    print(selection_mmr(documents, "délai de retour et remboursement", 2))
