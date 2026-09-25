"""Exécuter un juge OpenAI et conserver sa justification."""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag_en_pratique.observability import PROMPT_JUGE_FAITHFULNESS
from rag_en_pratique.prompting import generer, openai_configure


@dataclass(frozen=True)
class Verdict:
    note: float
    note_brute: int
    justification: str
    sortie_brute: str


def juger(
    question: str,
    contexte: str,
    reponse: str,
    *,
    client=None,
    model: str | None = None,
) -> Verdict:
    sortie = generer(
        "Respecte exactement la procédure et le format demandés.",
        PROMPT_JUGE_FAITHFULNESS.format(
            contexte=contexte[:3000],
            question=question,
            reponse=reponse,
        ),
        client=client,
        model=model,
    )
    note_match = re.search(r"NOTE\s*:\s*([1-5])", sortie, re.IGNORECASE)
    if not note_match:
        raise ValueError("Le juge n'a pas produit de note valide")
    note_brute = int(note_match.group(1))
    justification = re.search(
        r"JUSTIFICATION\s*:\s*(.+?)(?=NOTE\s*:)",
        sortie,
        re.DOTALL | re.IGNORECASE,
    )
    return Verdict(
        note=(note_brute - 1) / 4,
        note_brute=note_brute,
        justification=justification.group(1).strip() if justification else sortie[:300],
        sortie_brute=sortie,
    )


if __name__ == "__main__" and not openai_configure():
    print("Exemple prêt : configurez OPENAI_API_KEY et OPENAI_MODEL.")
