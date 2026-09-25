"""Contextual Retrieval avec OpenAI, uniquement lorsque la clé est disponible."""

import os
from typing import Protocol

GABARIT = """Voici un document complet :
<document>{document}</document>

Voici un extrait de ce document :
<extrait>{chunk}</extrait>

Rédige en une à deux phrases le contexte nécessaire pour situer cet extrait
dans le document. Ne réponds que par ces phrases, sans préambule."""


class Generateur(Protocol):
    def generer(self, prompt: str) -> str: ...


class GenerateurOpenAI:
    """Adaptateur minimal pour la Responses API."""

    def __init__(self, model: str | None = None) -> None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
        self.model = model or os.getenv("OPENAI_MODEL")
        if not self.model:
            raise RuntimeError("OPENAI_MODEL n'est pas configuré")
        from openai import OpenAI

        self.client = OpenAI()

    def generer(self, prompt: str) -> str:
        response = self.client.responses.create(model=self.model, input=prompt)
        return response.output_text


def contextualiser(document: str, chunks: list[str], llm: Generateur) -> list[str]:
    """Préfixe chaque chunk d'un contexte généré à partir du document complet."""

    enrichis: list[str] = []
    for chunk in chunks:
        contexte = llm.generer(GABARIT.format(document=document, chunk=chunk))
        enrichis.append(f"{contexte.strip()}\n\n{chunk}")
    return enrichis


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple facultatif : configurez OPENAI_API_KEY et OPENAI_MODEL pour l'exécuter.")
    else:
        document = "Politique 2026. Les retours sont acceptés sous trente jours avec un reçu."
        print(contextualiser(document, ["Ils exigent un reçu."], GenerateurOpenAI())[0])
