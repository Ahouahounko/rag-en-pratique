"""Pipeline de retrieval complet : réparer, chercher, fusionner et raffiner."""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Passage:
    texte: str
    source: str
    score: float


def fusion_rrf(listes: list[list[Passage]], constante: int = 60) -> list[Passage]:
    scores: dict[tuple[str, str], float] = {}
    passages: dict[tuple[str, str], Passage] = {}
    for resultats in listes:
        for rang, passage in enumerate(resultats, start=1):
            cle = (passage.source, passage.texte)
            passages[cle] = passage
            scores[cle] = scores.get(cle, 0.0) + 1.0 / (constante + rang)
    ordre = sorted(scores, key=scores.get, reverse=True)  # type: ignore[arg-type]
    return [passages[cle] for cle in ordre]


def reordonner_en_v(passages: list[Passage]) -> list[Passage]:
    return passages[::2] + passages[1::2][::-1]


def pipeline_retrieval(
    question: str,
    recherches: list[Callable[[str], list[Passage]]],
    *,
    variantes: list[str] | None = None,
    seuil: float = 0.2,
    k: int = 5,
) -> list[Passage]:
    """Orchestre les étapes dans un ordre explicite et testable."""

    requetes = [question, *(variantes or [])]
    listes = [recherche(requete) for requete in requetes for recherche in recherches]
    candidats = fusion_rrf(listes)[:30]
    candidats = sorted(candidats, key=lambda passage: passage.score, reverse=True)
    candidats = [passage for passage in candidats if passage.score >= seuil][:k]
    return reordonner_en_v(candidats)


if __name__ == "__main__":
    corpus = [
        Passage("Retour possible sous trente jours.", "retours.md", 0.95),
        Passage("Remboursement sous cinq jours.", "remboursement.md", 0.80),
        Passage("Livraison standard.", "livraison.md", 0.10),
    ]

    def recherche_locale(question: str) -> list[Passage]:
        del question
        return corpus

    print(pipeline_retrieval("Quel délai de retour ?", [recherche_locale], k=2))
