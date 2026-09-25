"""RAG itératif borné pour les questions nécessitant plusieurs recherches."""

from __future__ import annotations

import os
from typing import Any


def demander(client: Any, model: str, instruction: str) -> str:
    return client.responses.create(model=model, input=instruction).output_text.strip()


def rag_iteratif(
    question: str,
    retriever,
    max_iterations: int = 3,
    *,
    client: Any | None = None,
    model: str | None = None,
) -> dict[str, object]:
    if client is None:
        from openai import OpenAI

        client = OpenAI()
    model = model or os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Définissez OPENAI_MODEL.")

    contexte: list[Any] = []
    requete = question
    tours = 0
    for tours in range(1, max_iterations + 1):
        contexte.extend(retriever.invoke(requete))
        texte = "\n\n".join(document.page_content for document in contexte[:8])
        verdict = demander(
            client,
            model,
            f"Question : {question}\nContexte : {texte[:3000]}\n"
            "Réponds SUFFISANT ou MANQUE: <sous-question précise>.",
        )
        if verdict.startswith("SUFFISANT"):
            break
        if verdict.startswith("MANQUE:"):
            requete = verdict.split(":", 1)[1].strip()
        else:
            break
    texte = "\n\n".join(document.page_content for document in contexte[:8])
    reponse = demander(
        client,
        model,
        f"Contexte : {texte[:4000]}\nQuestion : {question}\nRéponds avec les sources.",
    )
    return {"reponse": reponse, "tours": tours, "sources": contexte}


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple prêt : définissez OPENAI_API_KEY et OPENAI_MODEL.")
