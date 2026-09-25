"""Évaluation d'une réponse RAG par le fournisseur configuré."""

from __future__ import annotations

from rag_en_pratique.core import Document, SearchResult
from rag_en_pratique.providers import create_generator


def evaluate_grounding(question: str, context: str, answer: str) -> str:
    judge_question = (
        "Évalue si la réponse candidate est entièrement fondée sur le contexte. "
        "Réponds par VALIDE ou INVALIDE, puis justifie brièvement.\n\n"
        f"Question initiale : {question}\nRéponse candidate : {answer}"
    )
    passage = SearchResult(Document(context, {"source": "contexte_evaluation"}), 1.0)
    return create_generator().generate(judge_question, [passage])


if __name__ == "__main__":
    verdict = evaluate_grounding(
        "Quel est le délai de retour ?",
        "Les retours sont acceptés sous 30 jours.",
        "Le délai de retour est de 30 jours.",
    )
    print(verdict)
