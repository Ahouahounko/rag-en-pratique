"""Filtrer et annoter les passages selon leur pertinence."""

from __future__ import annotations

from rag_en_pratique.prompting import Passage


def formater_avec_pertinence(
    passages: list[Passage],
    scores: list[float],
    seuil: float = 0.5,
) -> str:
    if len(passages) != len(scores):
        raise ValueError("Un score est requis pour chaque passage")
    blocs = []
    for passage, score in zip(passages, scores, strict=True):
        if score < seuil:
            continue
        if score >= 0.85:
            niveau = "correspondance forte"
        elif score >= 0.70:
            niveau = "correspondance moyenne"
        else:
            niveau = "correspondance faible — à confirmer"
        numero = len(blocs) + 1
        source = passage.metadata.get("source", "inconnu")
        blocs.append(f"[doc_{numero}] {source} ({niveau})\n{passage.page_content}")
    return "\n\n---\n\n".join(blocs) or "Aucun extrait ne dépasse le seuil de pertinence."


if __name__ == "__main__":
    passages = [Passage("Retour sous 30 jours.", {"source": "cgv.pdf"})]
    print(formater_avec_pertinence(passages, [0.91]))
