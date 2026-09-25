"""Attribuer les défaillances au retriever, au générateur ou à l'ancrage."""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from typing import Any


def _identifiant(source: Any) -> str:
    if hasattr(source, "id"):
        return str(source.id)
    return str(source.metadata.get("id", source.metadata.get("source", "")))


def attribuer_defaillances(
    jeu: list[dict[str, object]],
    systeme,
    juger_exactitude: Callable[[str, str, str], bool],
) -> dict[str, object]:
    compteurs: Counter[str] = Counter()
    exemples = {nom: [] for nom in ("generateur", "retriever", "ancrage", "nominal")}
    for entree in jeu:
        question = str(entree["question"])
        sortie = systeme.repondre(question)
        obtenus = {_identifiant(source) for source in sortie["sources"]}
        attendus = {str(item) for item in entree["passages_attendus"]}
        retrieval_ok = bool(attendus & obtenus) if attendus else not obtenus
        reponse_ok = juger_exactitude(question, sortie["reponse"], str(entree["reponse"]))
        if retrieval_ok and reponse_ok:
            categorie = "nominal"
        elif retrieval_ok:
            categorie = "generateur"
        elif not reponse_ok:
            categorie = "retriever"
        else:
            categorie = "ancrage"
        compteurs[categorie] += 1
        exemples[categorie].append(question)
    total = sum(compteurs.values())
    repartition = {
        nom: round(compteurs[nom] / total, 3) if total else 0.0 for nom in exemples
    }
    priorite = "retriever" if compteurs["retriever"] >= compteurs["generateur"] else "generateur"
    return {
        "repartition": repartition,
        "priorite": priorite,
        "alerte_ancrage": repartition["ancrage"] > 0.05,
        "exemples": exemples,
    }


if __name__ == "__main__":
    print("Injectez un système RAG et une fonction d'exactitude dans attribuer_defaillances().")
