"""Exécuter une campagne d'évaluation RAG et produire un diagnostic."""

from __future__ import annotations

import statistics
from collections.abc import Callable
from typing import Any

from rag_en_pratique.prompting import generer, openai_configure

SEUILS = {
    "faithfulness": 0.80,
    "answer_relevance": 0.75,
    "contextual_precision": 0.65,
    "contextual_recall": 0.70,
}


def diagnostiquer(moyennes: dict[str, float], seuils: dict[str, float] | None = None) -> str:
    s = seuils or SEUILS
    bas = {nom for nom, seuil in s.items() if moyennes.get(nom, 0.0) < seuil}
    if not bas:
        return "Système sain. Surveiller sans intervenir."
    if "faithfulness" in bas and "answer_relevance" not in bas:
        return "Hallucination à la génération : renforcer l'ancrage du prompt."
    if "answer_relevance" in bas and "contextual_recall" not in bas:
        return "Échec à la génération : revoir le prompt, le format ou le modèle."
    if {"contextual_precision", "contextual_recall"} <= bas:
        return "Échec au retrieval : vérifier le corpus avant d'optimiser le retriever."
    if bas == {"contextual_precision"}:
        return "Retriever bruyant : reclasser, réduire k ou relever le seuil."
    if bas == {"contextual_recall"}:
        return "Retriever incomplet : recherche hybride, k plus grand ou nouveau découpage."
    if len(bas) >= 3:
        return "Défaut systémique : reprendre depuis l'ingestion."
    return f"Configuration mixte, métriques basses : {sorted(bas)}"


def score_juge(
    critere: str,
    question: str,
    contenu: str,
    *,
    client=None,
    model: str | None = None,
) -> float:
    texte = generer(
        "Évalue selon le critère demandé. Réponds uniquement par un nombre entre 0 et 1.",
        f"CRITÈRE : {critere}\nQUESTION : {question}\nCONTENU :\n{contenu}",
        client=client,
        model=model,
    )
    try:
        return max(0.0, min(1.0, float(texte.replace(",", "."))))
    except ValueError as erreur:
        raise ValueError(f"Score du juge invalide : {texte!r}") from erreur


def rappel_contextuel(attendus: set[str], sources: list[Any]) -> float:
    if not attendus:
        return 1.0
    recuperes = {
        str(source.metadata.get("id", source.metadata.get("source", ""))) for source in sources
    }
    return len(attendus & recuperes) / len(attendus)


def lancer_campagne(
    jeu: list[dict[str, Any]],
    systeme,
    metadonnees: dict[str, str],
    *,
    faithfulness: Callable[[str, str], float],
    answer_relevance: Callable[[str, str], float],
    contextual_precision: Callable[[str, list[Any]], float],
) -> dict[str, object]:
    par_metrique: dict[str, list[float]] = {nom: [] for nom in SEUILS}
    par_cas = []
    for cas in jeu:
        sortie = systeme.repondre(cas["question"])
        sources = list(sortie["sources"])
        contexte = "\n\n".join(source.page_content for source in sources)
        scores = {
            "faithfulness": faithfulness(sortie["reponse"], contexte),
            "answer_relevance": answer_relevance(cas["question"], sortie["reponse"]),
            "contextual_precision": contextual_precision(cas["question"], sources),
            "contextual_recall": rappel_contextuel(set(cas["passages_attendus"]), sources),
        }
        for nom, valeur in scores.items():
            par_metrique[nom].append(valeur)
        par_cas.append(
            {**scores, "question": cas["question"], "type": cas.get("type"), "sujet": cas.get("sujet")}
        )
    moyennes = {
        nom: round(statistics.mean(valeurs), 3)
        for nom, valeurs in par_metrique.items()
        if valeurs
    }
    return {
        "moyennes": moyennes,
        "diagnostic": diagnostiquer(moyennes),
        "par_cas": par_cas,
        "metadonnees": metadonnees,
    }


if __name__ == "__main__":
    if openai_configure():
        print("Injectez votre système RAG et les trois fonctions de mesure dans lancer_campagne().")
    else:
        print("La campagne est prête ; les métriques locales n'exigent aucune clé.")
