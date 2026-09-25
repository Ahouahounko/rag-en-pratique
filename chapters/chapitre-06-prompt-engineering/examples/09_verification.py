"""Vérifier l'ancrage d'une réponse, affirmation par affirmation."""

from __future__ import annotations

from rag_en_pratique.prompting import generer, openai_configure

INSTRUCTIONS = """Compare le texte aux extraits, sans juger sa qualité.
Pour chaque affirmation, écris : AFFIRMATION | ÉTAYÉE | PARTIELLE | ABSENTE.
Termine par VERDICT: FIABLE uniquement si chaque affirmation est étayée ; sinon VERDICT: À REVOIR."""


def verifier_ancrage(
    reponse: str,
    contexte: str,
    *,
    client=None,
    model: str | None = None,
) -> dict[str, object]:
    verdict = generer(
        INSTRUCTIONS,
        f"EXTRAITS DE RÉFÉRENCE :\n{contexte}\n\nTEXTE À VÉRIFIER :\n{reponse}",
        client=client,
        model=model,
    )
    return {"detail": verdict, "fiable": "VERDICT: FIABLE" in verdict}


if __name__ == "__main__" and not openai_configure():
    print("Exemple prêt : configurez OPENAI_API_KEY et OPENAI_MODEL.")
