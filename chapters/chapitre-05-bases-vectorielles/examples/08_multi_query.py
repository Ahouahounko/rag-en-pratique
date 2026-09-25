"""Générer plusieurs formulations et fusionner leurs classements avec RRF."""

from __future__ import annotations

import os
from collections import defaultdict
from collections.abc import Callable, Hashable
from typing import Any, TypeVar

T = TypeVar("T", bound=Hashable)


def generer_variantes(
    question: str,
    nombre: int = 3,
    *,
    client: Any | None = None,
    model: str | None = None,
) -> list[str]:
    if client is None:
        from openai import OpenAI

        client = OpenAI()
    model = model or os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Définissez OPENAI_MODEL.")
    reponse = client.responses.create(
        model=model,
        input=f"Reformule cette question de {nombre} façons. Une formulation par ligne : {question}",
    )
    variantes = [ligne.strip(" -0123456789.") for ligne in reponse.output_text.splitlines()]
    return [question, *[variante for variante in variantes if variante][:nombre]]


def fusion_rrf(classements: list[list[T]], constante: int = 60) -> list[T]:
    scores: dict[T, float] = defaultdict(float)
    for classement in classements:
        for rang, element in enumerate(classement, start=1):
            scores[element] += 1 / (constante + rang)
    return sorted(scores, key=scores.get, reverse=True)


def multi_query(
    question: str,
    rechercher: Callable[[str], list[T]],
    *,
    client: Any | None = None,
    model: str | None = None,
) -> list[T]:
    requetes = generer_variantes(question, client=client, model=model)
    return fusion_rrf([rechercher(requete) for requete in requetes])


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple prêt : définissez OPENAI_API_KEY et OPENAI_MODEL.")
    else:
        documents = ["retour sous 30 jours", "garantie de 24 mois", "remboursement"]
        recherche = lambda q: sorted(documents, key=lambda d: len(set(q.split()) & set(d.split())), reverse=True)
        print(multi_query("Quel est le délai de retour ?", recherche))
