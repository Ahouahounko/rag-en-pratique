"""Compression contextuelle par extraction avec OpenAI."""

import os
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class Passage:
    page_content: str
    source: str


class Retriever(Protocol):
    def invoke(self, question: str) -> list[Passage]: ...


def compresser_passage(
    question: str,
    passage: Passage,
    *,
    client: Any = None,
    model: str | None = None,
) -> Passage | None:
    if client is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
        from openai import OpenAI

        client = OpenAI()
    response = client.responses.create(
        model=model or os.getenv("OPENAI_MODEL"),
        instructions=(
            "Extrais uniquement les phrases utiles pour répondre à la question. "
            "Si rien n'est utile, réponds exactement HORS_SUJET."
        ),
        input=f"QUESTION\n{question}\n\nPASSAGE\n{passage.page_content}",
    )
    texte = response.output_text.strip()
    return None if texte == "HORS_SUJET" else Passage(texte, passage.source)


def rechercher_et_compresser(
    question: str,
    retriever: Retriever,
    *,
    client: Any = None,
) -> list[Passage]:
    compresses = [
        compresser_passage(question, passage, client=client)
        for passage in retriever.invoke(question)
    ]
    return [passage for passage in compresses if passage is not None]


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple facultatif : configurez OPENAI_API_KEY et OPENAI_MODEL.")
    else:
        class RetrieverExemple:
            def invoke(self, question: str) -> list[Passage]:
                del question
                return [
                    Passage(
                        "Les retours sont acceptés sous trente jours. "
                        "Le service client est ouvert le lundi.",
                        "retours.md",
                    )
                ]

        print(rechercher_et_compresser("Quel est le délai de retour ?", RetrieverExemple()))
