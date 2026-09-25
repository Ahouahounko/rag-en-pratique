"""Filtrer des questions synthétiques selon leur réalisme."""

from __future__ import annotations

from rag_en_pratique.observability import extraire_note
from rag_en_pratique.prompting import generer, openai_configure

INSTRUCTIONS = """Note le réalisme d'une question de recherche immobilière de 1 à 5.
5 = formulation naturelle et besoin plausible ; 1 = détail absurde ou demande artificielle.
Réponds avec une brève explication, puis une ligne « Note : N »."""


def filtrer(
    questions: list[dict[str, object]],
    note_minimale: int = 4,
    *,
    client=None,
    model: str | None = None,
) -> list[dict[str, object]]:
    retenues = []
    for question in questions:
        sortie = generer(
            INSTRUCTIONS,
            f"QUESTION : {question['question']}",
            client=client,
            model=model,
        )
        note = extraire_note(sortie)
        if note >= note_minimale:
            retenues.append({**question, "note_realisme": note, "justification": sortie})
    return retenues


if __name__ == "__main__" and not openai_configure():
    print("Exemple prêt : configurez OPENAI_API_KEY et OPENAI_MODEL.")
