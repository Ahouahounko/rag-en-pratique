"""Tester si un système RAG dépend réellement du contexte fourni."""

from __future__ import annotations

import random
import re


def similarite_lexicale(premier: str, second: str) -> float:
    a = set(re.findall(r"\w+", premier.lower()))
    b = set(re.findall(r"\w+", second.lower()))
    return len(a & b) / len(a | b) if a or b else 1.0


def est_une_abstention(texte: str) -> bool:
    normalise = texte.lower()
    marqueurs = (
        "ne permettent pas de répondre",
        "information absente",
        "je ne peux pas répondre",
        "abstention",
    )
    return any(marqueur in normalise for marqueur in marqueurs)


def tester_ancrage(
    jeu: list[dict[str, object]],
    systeme,
    corpus_etranger: list[object],
    seuil_similarite: float = 0.75,
    *,
    taille_contexte: int = 5,
    graine: int = 42,
) -> dict[str, object]:
    if not jeu:
        raise ValueError("Le jeu d'évaluation ne peut pas être vide")
    if not corpus_etranger:
        raise ValueError("Le corpus étranger ne peut pas être vide")
    rng = random.Random(graine)
    identiques = abstentions = 0
    for entree in jeu:
        question = str(entree["question"])
        reponse_reelle = systeme.repondre(question)["reponse"]
        contexte = rng.sample(corpus_etranger, min(taille_contexte, len(corpus_etranger)))
        reponse_substituee = systeme.generer_avec(question, contexte=contexte)
        if est_une_abstention(reponse_substituee):
            abstentions += 1
        elif similarite_lexicale(reponse_reelle, reponse_substituee) > seuil_similarite:
            identiques += 1
    total = len(jeu)
    taux_abstention = abstentions / total
    return {
        "taux_abstention": round(taux_abstention, 3),
        "taux_reponse_de_memoire": round(identiques / total, 3),
        "ancrage_suffisant": taux_abstention > 0.85,
    }


if __name__ == "__main__":
    print(round(similarite_lexicale("garantie 24 mois", "garantie de 24 mois"), 3))
