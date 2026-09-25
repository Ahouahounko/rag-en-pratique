"""Générer un jeu de référence équilibré à partir d'un corpus."""

from __future__ import annotations

import itertools
import random
from collections import defaultdict

from rag_en_pratique.observability import PassageEvaluation
from rag_en_pratique.prompting import generer, openai_configure


def _tirer(elements: list, nombre: int, rng: random.Random) -> list:
    if not elements or nombre <= 0:
        return []
    return rng.sample(elements, min(nombre, len(elements)))


def generer_jeu(
    passages: list[PassageEvaluation],
    taille: int,
    repartition: dict[str, float],
    sujets_voisins: list[str],
    *,
    client=None,
    model: str | None = None,
    graine: int = 42,
) -> list[dict[str, object]]:
    """Crée des questions directes, de synthèse et sans réponse."""
    if taille <= 0:
        raise ValueError("taille doit être positive")
    types = ("directe", "synthese", "sans_reponse")
    if set(repartition) != set(types) or abs(sum(repartition.values()) - 1.0) > 1e-9:
        raise ValueError(f"La répartition doit contenir {types} et totaliser 1")
    rng = random.Random(graine)
    comptes = {nom: int(taille * repartition[nom]) for nom in types}
    comptes["directe"] += taille - sum(comptes.values())
    jeu: list[dict[str, object]] = []

    for passage in _tirer(passages, comptes["directe"], rng):
        question = generer(
            "Écris une question réaliste dont la réponse est entièrement dans le passage.",
            passage.texte,
            client=client,
            model=model,
        )
        reponse = generer(
            "Réponds uniquement avec le passage fourni.",
            f"PASSAGE : {passage.texte}\nQUESTION : {question}",
            client=client,
            model=model,
        )
        jeu.append(
            {
                "question": question,
                "reponse": reponse,
                "passages_attendus": [passage.id],
                "type": "directe",
            }
        )

    par_source: dict[str, list[PassageEvaluation]] = defaultdict(list)
    for passage in passages:
        par_source[passage.source].append(passage)
    couples = [
        couple
        for groupe in par_source.values()
        for couple in itertools.combinations(groupe, 2)
    ]
    for premier, second in _tirer(couples, comptes["synthese"], rng):
        question = generer(
            "Écris une question réaliste qui exige les deux passages pour répondre complètement.",
            f"PASSAGE 1 : {premier.texte}\nPASSAGE 2 : {second.texte}",
            client=client,
            model=model,
        )
        reponse = generer(
            "Réponds uniquement avec les deux passages.",
            f"PASSAGES : {premier.texte}\n{second.texte}\nQUESTION : {question}",
            client=client,
            model=model,
        )
        jeu.append(
            {
                "question": question,
                "reponse": reponse,
                "passages_attendus": [premier.id, second.id],
                "type": "synthese",
            }
        )

    for sujet in _tirer(sujets_voisins, comptes["sans_reponse"], rng):
        question = generer(
            "Écris une question plausible dont la réponse n'est pas dans le corpus.",
            f"SUJET VOISIN : {sujet}",
            client=client,
            model=model,
        )
        jeu.append(
            {
                "question": question,
                "reponse": "ABSTENTION_ATTENDUE",
                "passages_attendus": [],
                "type": "sans_reponse",
            }
        )
    return jeu


if __name__ == "__main__" and not openai_configure():
    print("Exemple prêt : configurez OPENAI_API_KEY et OPENAI_MODEL pour générer le jeu.")
