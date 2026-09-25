"""Décider s'il faut chercher, répondre directement ou clarifier."""

from __future__ import annotations

import os
from enum import Enum
from typing import Any


class Decision(Enum):
    CHERCHER = "chercher"
    REPONDRE = "repondre"
    CLARIFIER = "clarifier"


def decider(
    question: str,
    *,
    client: Any | None = None,
    model: str | None = None,
) -> Decision:
    if client is None:
        from openai import OpenAI

        client = OpenAI()
    model = model or os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Définissez OPENAI_MODEL.")
    reponse = client.responses.create(
        model=model,
        input=(
            f"Question : {question}\n"
            "Réponds par chercher pour des données internes/récentes, repondre pour un concept "
            "stable, ou clarifier si la question est ambiguë. Un seul mot."
        ),
    )
    try:
        return Decision(reponse.output_text.strip().lower())
    except ValueError:
        return Decision.CHERCHER


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple prêt : définissez OPENAI_API_KEY et OPENAI_MODEL.")
    else:
        print(decider("Quel est le chiffre d'affaires interne de cette année ?"))
