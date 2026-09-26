"""Routage économique en deux étages avec génération OpenAI."""

from __future__ import annotations

import os
from collections.abc import Callable
from enum import Enum


class Complexite(Enum):
    SIMPLE = "simple"
    MOYENNE = "moyenne"
    COMPLEXE = "complexe"


SUJETS_CRITIQUES = (
    "juridique",
    "medical",
    "médical",
    "contrat",
    "sanction",
    "licenciement",
    "conformite",
    "conformité",
)
MARQUEURS_SIMPLES = ("quel est", "combien", "quand", "qui est", "quel montant")
MARQUEURS_COMPLEXES = (
    "compare",
    "implique",
    "synthèse",
    "synthese",
    "analyse",
    "impact de",
    "différence entre",
    "difference entre",
    "pourquoi",
)


def classer(
    question: str,
    classifieur: Callable[[str], str] | None = None,
) -> Complexite:
    texte = question.casefold()
    if any(sujet in texte for sujet in SUJETS_CRITIQUES):
        return Complexite.COMPLEXE
    if any(marker in texte for marker in MARQUEURS_COMPLEXES):
        return Complexite.COMPLEXE
    if any(marker in texte for marker in MARQUEURS_SIMPLES) and len(texte.split()) < 15:
        return Complexite.SIMPLE
    if classifieur is None:
        return Complexite.MOYENNE
    try:
        return Complexite(classifieur(question).strip().lower())
    except ValueError:
        return Complexite.MOYENNE


def modele_pour(complexite: Complexite) -> str:
    small = os.getenv("OPENAI_SMALL_MODEL") or os.getenv("OPENAI_MODEL")
    large = os.getenv("OPENAI_LARGE_MODEL") or os.getenv("OPENAI_MODEL")
    selected = large if complexite is Complexite.COMPLEXE else small
    if not selected:
        raise RuntimeError("Configurez OPENAI_MODEL ou les variantes SMALL/LARGE")
    return selected


def repondre(
    question: str,
    *,
    instructions: str,
    classifieur: Callable[[str], str] | None = None,
    client=None,
) -> tuple[str, Complexite, str]:
    complexity = classer(question, classifieur)
    model = modele_pour(complexity)
    if client is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
        from openai import OpenAI

        client = OpenAI()
    response = client.responses.create(model=model, instructions=instructions, input=question)
    return str(response.output_text), complexity, model


if __name__ == "__main__":
    for example in ("Quel est le délai ?", "Compare les trois politiques", "Explique la règle"):
        print(example, "->", classer(example).value)
