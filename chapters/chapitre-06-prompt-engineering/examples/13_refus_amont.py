"""Refuser avant génération quand aucun passage n'est assez pertinent."""

from __future__ import annotations

from rag_en_pratique.prompting import formater_simple, generer, openai_configure

REFUS = "Les documents fournis ne permettent pas de répondre à cette question."


def repondre_avec_garde_fou(
    question: str,
    retriever,
    seuil_minimal: float = 0.35,
    *,
    client=None,
    model: str | None = None,
) -> dict[str, object]:
    passages = list(retriever.invoke(question))
    meilleur = max(
        (passage.metadata.get("score_reclassement", 0.0) for passage in passages),
        default=0.0,
    )
    if meilleur < seuil_minimal:
        return {"reponse": REFUS, "confiance": "nulle", "sources": [], "modele_appele": False}
    reponse = generer(
        "Réponds uniquement avec les extraits et cite chaque affirmation.",
        f"EXTRAITS :\n{formater_simple(passages)}\n\nQUESTION : {question}",
        client=client,
        model=model,
    )
    confiance = "élevée" if meilleur > 0.7 else "moyenne" if meilleur > 0.5 else "faible"
    return {
        "reponse": reponse,
        "confiance": confiance,
        "sources": passages,
        "modele_appele": True,
    }


if __name__ == "__main__" and not openai_configure():
    print("Le garde-fou peut refuser sans configurer OpenAI.")
