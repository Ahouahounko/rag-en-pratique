"""Orienter une question vers des documents, des tables ou les deux."""

from __future__ import annotations

import os
from enum import Enum
from typing import Any


class Source(Enum):
    DOCUMENTS = "documents"
    TABLES = "tables"
    LES_DEUX = "les_deux"


GABARIT = """Détermine où chercher la réponse.
- documents : procédures, politiques, explications, définitions
- tables : chiffres, comptages, agrégats, évolutions datées
- les_deux : un chiffre et son explication
Question : {question}
Réponds par un seul mot."""


def router(
    question: str,
    *,
    client: Any | None = None,
    model: str | None = None,
) -> Source:
    if client is None:
        from openai import OpenAI

        client = OpenAI()
    model = model or os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Définissez OPENAI_MODEL.")
    reponse = client.responses.create(model=model, input=GABARIT.format(question=question))
    try:
        return Source(reponse.output_text.strip().lower())
    except ValueError:
        return Source.DOCUMENTS


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple prêt : définissez OPENAI_API_KEY et OPENAI_MODEL.")
    else:
        print(router("Combien de ventes ont été réalisées et pourquoi ?"))
