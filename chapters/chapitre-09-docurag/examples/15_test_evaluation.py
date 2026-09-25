"""Évaluation d'une réponse RAG par un juge OpenAI."""

from __future__ import annotations

import os

from openai import OpenAI


def evaluate_grounding(question: str, context: str, answer: str) -> str:
    model = os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError("OPENAI_MODEL n'est pas configuré")
    response = OpenAI().responses.create(
        model=model,
        instructions=(
            "Tu es un juge RAG. Évalue si la réponse est entièrement fondée "
            "sur le contexte. Réponds par VALIDE ou INVALIDE, puis justifie brièvement."
        ),
        input=f"QUESTION\n{question}\n\nCONTEXTE\n{context}\n\nRÉPONSE\n{answer}",
    )
    return response.output_text


if __name__ == "__main__":
    verdict = evaluate_grounding(
        "Quel est le délai de retour ?",
        "Les retours sont acceptés sous 30 jours.",
        "Le délai de retour est de 30 jours.",
    )
    print(verdict)
