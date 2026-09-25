"""Produire une synthèse organisée par thèmes plutôt que par documents."""

from __future__ import annotations

from rag_en_pratique.prompting import generer, openai_configure

INSTRUCTIONS_SYNTHESE = """Produis une synthèse documentaire.
1. Identifie les thèmes transversaux.
2. Organise la réponse par thème, jamais par document.
3. Rassemble les apports en citant chaque source.
4. Ne répète pas une information commune : regroupe ses citations.
5. Termine par « Points non couverts ».
Structure : **Synthèse**, puis **Points non couverts**."""


def synthetiser(
    contexte: str,
    question: str,
    nb_extraits: int,
    *,
    client=None,
    model: str | None = None,
) -> str:
    return generer(
        INSTRUCTIONS_SYNTHESE,
        f"EXTRAITS ({nb_extraits} sources) :\n{contexte}\n\nQUESTION : {question}",
        client=client,
        model=model,
    )


if __name__ == "__main__":
    if openai_configure():
        print(synthetiser("[doc_1] Retour 30 jours.", "Résume la politique.", 1))
    else:
        print(INSTRUCTIONS_SYNTHESE)
