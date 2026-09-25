"""Query Expansion avec OpenAI, puis fusion locale par RRF."""

import os
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class Passage:
    page_content: str
    source: str


class Retriever(Protocol):
    def invoke(self, question: str) -> list[Passage]: ...


def generer_variantes(
    question: str,
    n: int = 3,
    *,
    client: Any = None,
    model: str | None = None,
) -> list[str]:
    """Produit plusieurs formulations et conserve la question d'origine."""

    if client is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
        from openai import OpenAI

        client = OpenAI()
    response = client.responses.create(
        model=model or os.getenv("OPENAI_MODEL"),
        instructions="Retourne uniquement les reformulations, une par ligne.",
        input=(
            f"Génère {n} reformulations de cette question avec des synonymes métier, "
            f"un angle plus général et un angle plus précis :\n{question}"
        ),
    )
    variantes = [ligne.strip(" -0123456789.") for ligne in response.output_text.splitlines()]
    return [question, *[variante for variante in variantes if variante]][: n + 1]


def fusion_rrf(listes: list[list[Passage]], constante: int = 60) -> list[Passage]:
    """Fusionne des classements incompatibles à partir de leurs rangs."""

    cumul: dict[tuple[str, str], dict[str, object]] = {}
    for resultats in listes:
        for rang, passage in enumerate(resultats, start=1):
            cle = (passage.source, passage.page_content)
            entree = cumul.setdefault(cle, {"score": 0.0, "passage": passage})
            entree["score"] = float(entree["score"]) + 1.0 / (constante + rang)
    classes = sorted(cumul.values(), key=lambda item: float(item["score"]), reverse=True)
    return [item["passage"] for item in classes]  # type: ignore[misc]


def recherche_elargie(question: str, retriever: Retriever, variantes: list[str], k: int = 5) -> list[Passage]:
    return fusion_rrf([retriever.invoke(variante) for variante in [question, *variantes]])[:k]


if __name__ == "__main__":
    listes = [
        [Passage("Retour sous 30 jours", "retours.md"), Passage("Livraison en 5 jours", "livraison.md")],
        [Passage("Livraison en 5 jours", "livraison.md"), Passage("Retour sous 30 jours", "retours.md")],
    ]
    print("Démonstration RRF :", [passage.source for passage in fusion_rrf(listes)])
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Expansion OpenAI facultative : configurez OPENAI_API_KEY et OPENAI_MODEL.")
    else:
        print("Variantes OpenAI :", generer_variantes("Quel est le délai de retour ?"))
