"""Construire un refus gradué selon la couverture des extraits."""

from __future__ import annotations

from rag_en_pratique.prompting import generer, openai_configure

INSTRUCTIONS_REFUS = """Tu es un assistant documentaire.
- Couverture complète : réponds et cite.
- Couverture partielle : réponds sur ce qui est couvert, puis écris « Non couvert par les documents : ... ».
- Aucune couverture : écris exactement « Les documents fournis ne permettent pas de répondre à cette question. »
Ne transforme jamais une hypothèse en fait et n'utilise pas ta mémoire pour compléter les extraits."""


def repondre_avec_refus(
    contexte: str,
    question: str,
    *,
    client=None,
    model: str | None = None,
) -> str:
    return generer(
        INSTRUCTIONS_REFUS,
        f"EXTRAITS :\n{contexte}\n\nQUESTION : {question}",
        client=client,
        model=model,
    )


if __name__ == "__main__":
    if openai_configure():
        print(repondre_avec_refus("Garantie 24 mois.", "Est-elle transférable ?"))
    else:
        print(INSTRUCTIONS_REFUS)
