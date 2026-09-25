"""HyDE : rechercher avec l'embedding d'un document hypothétique OpenAI."""

import math
import os
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Passage:
    texte: str
    source: str


def vecteur_mots(texte: str, vocabulaire: list[str]) -> list[float]:
    compte = Counter(re.findall(r"\w+", texte.lower()))
    return [float(compte[mot]) for mot in vocabulaire]


def cosinus(gauche: list[float], droite: list[float]) -> float:
    produit = sum(a * b for a, b in zip(gauche, droite, strict=True))
    norme_g = math.sqrt(sum(valeur**2 for valeur in gauche))
    norme_d = math.sqrt(sum(valeur**2 for valeur in droite))
    return produit / (norme_g * norme_d) if norme_g and norme_d else 0.0


def rediger_hypothese(question: str, *, client: Any = None, model: str | None = None) -> str:
    if client is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
        from openai import OpenAI

        client = OpenAI()
    response = client.responses.create(
        model=model or os.getenv("OPENAI_MODEL"),
        instructions=(
            "Rédige 3 à 5 phrases factuelles comme un manuel officiel. "
            "N'indique jamais qu'il s'agit d'une hypothèse."
        ),
        input=question,
    )
    return response.output_text


def recherche_hyde(question: str, corpus: list[Passage], *, client: Any = None, k: int = 3) -> list[Passage]:
    hypothese = rediger_hypothese(question, client=client)
    vocabulaire = sorted({mot for passage in corpus for mot in re.findall(r"\w+", passage.texte.lower())})
    vecteur_hypothese = vecteur_mots(hypothese, vocabulaire)
    return sorted(
        corpus,
        key=lambda passage: cosinus(vecteur_hypothese, vecteur_mots(passage.texte, vocabulaire)),
        reverse=True,
    )[:k]


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple facultatif : configurez OPENAI_API_KEY et OPENAI_MODEL.")
    else:
        documents = [
            Passage("Les retours sont acceptés sous trente jours.", "retours.md"),
            Passage("La livraison standard prend cinq jours.", "livraison.md"),
        ]
        print(recherche_hyde("Quel est le délai de retour ?", documents))
