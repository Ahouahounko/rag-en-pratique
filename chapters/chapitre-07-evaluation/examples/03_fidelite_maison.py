"""Mesurer la fidélité d'une réponse avec un juge OpenAI injectable."""

from __future__ import annotations

from rag_en_pratique.prompting import generer, openai_configure


def calculer_faithfulness(
    reponse: str,
    contexte: str,
    *,
    client=None,
    model: str | None = None,
) -> dict[str, object]:
    """Décompose la réponse, puis vérifie chaque affirmation contre le contexte."""
    brut = generer(
        "Décompose le texte en faits vérifiables, un par ligne, sans numérotation ni ajout.",
        reponse,
        client=client,
        model=model,
    )
    affirmations = [ligne.strip(" -•\t") for ligne in brut.splitlines() if ligne.strip()]
    if not affirmations:
        return {"score": 1.0, "detail": [], "total": 0}

    detail = []
    for affirmation in affirmations:
        verdict = generer(
            "Réponds par un seul mot : ETAYEE, PARTIELLE ou ABSENTE.",
            (
                f"PASSAGES :\n{contexte}\n\nAFFIRMATION : {affirmation}\n\n"
                "Peut-elle être déduite des passages ? Une information vraie mais absente est ABSENTE."
            ),
            client=client,
            model=model,
        ).upper()
        etiquette = verdict.split()[0] if verdict else "ABSENTE"
        poids = {"ETAYEE": 1.0, "ÉTAYÉE": 1.0, "PARTIELLE": 0.5}.get(etiquette, 0.0)
        detail.append({"affirmation": affirmation, "verdict": verdict, "poids": poids})
    return {
        "score": sum(item["poids"] for item in detail) / len(detail),
        "detail": detail,
        "total": len(detail),
    }


if __name__ == "__main__":
    if openai_configure():
        print(calculer_faithfulness("La garantie dure 24 mois.", "Garantie : 24 mois."))
    else:
        print("Exemple prêt : configurez OPENAI_API_KEY et OPENAI_MODEL.")
