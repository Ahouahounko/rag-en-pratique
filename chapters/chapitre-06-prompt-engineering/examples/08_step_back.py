"""Rechercher le principe général avant d'appliquer la règle au cas particulier."""

from __future__ import annotations

from rag_en_pratique.prompting import Passage, formater_simple, generer, openai_configure


def rag_step_back(
    question: str,
    retriever,
    *,
    client=None,
    model: str | None = None,
) -> str:
    generale = generer(
        "Formule une question générale visant la règle applicable. Ne réponds pas au cas.",
        f"Cas particulier : {question}",
        client=client,
        model=model,
    )
    specifiques = list(retriever.invoke(question))
    generaux = list(retriever.invoke(generale))
    textes_vus = {passage.page_content for passage in specifiques}
    tous: list[Passage] = specifiques + [
        passage for passage in generaux if passage.page_content not in textes_vus
    ]
    return generer(
        "Réponds à partir des extraits. Énonce la règle générale, puis son application. Cite.",
        f"EXTRAITS :\n{formater_simple(tous)}\n\nPRINCIPE : {generale}\nQUESTION : {question}",
        client=client,
        model=model,
    )


if __name__ == "__main__" and not openai_configure():
    print("Exemple prêt : configurez OPENAI_API_KEY et OPENAI_MODEL.")
