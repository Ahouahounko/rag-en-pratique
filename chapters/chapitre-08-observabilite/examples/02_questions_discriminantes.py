"""Générer une question qui sépare un passage de ses voisins proches."""

from __future__ import annotations

from rag_en_pratique.observability import PassageEvaluation, extraire_json
from rag_en_pratique.prompting import generer, openai_configure


def generer_question_discriminante(
    passage_cible: PassageEvaluation,
    index,
    n_distracteurs: int = 2,
    *,
    client=None,
    model: str | None = None,
) -> dict[str, object]:
    voisins = [
        passage
        for passage in index.chercher(passage_cible.texte, k=n_distracteurs + 1)
        if passage.id != passage_cible.id
    ][:n_distracteurs]
    distracteurs = "\n".join(
        f"[Distracteur {numero}] {passage.texte}"
        for numero, passage in enumerate(voisins, start=1)
    )
    sortie = generer(
        "Retourne uniquement un JSON avec les clés question et reponse.",
        (
            f"PASSAGE CIBLE :\n{passage_cible.texte}\n\nDISTRACTEURS :\n{distracteurs}\n\n"
            "Écris une question réaliste que seul le passage cible permet de résoudre, "
            "mais qui partage du vocabulaire avec les distracteurs."
        ),
        client=client,
        model=model,
    )
    resultat = extraire_json(sortie)
    return {
        "question": str(resultat["question"]),
        "reponse": str(resultat["reponse"]),
        "passages_attendus": [passage_cible.id],
        "distracteurs_connus": [passage.id for passage in voisins],
        "type": "discriminante",
    }


if __name__ == "__main__" and not openai_configure():
    print("Exemple prêt : configurez OpenAI et injectez votre index.")
