"""Construire le prompt RAG minimal viable et l'envoyer à OpenAI."""

from __future__ import annotations

from rag_en_pratique.prompting import Passage, formater_simple, generer, openai_configure

SYSTEME = """Tu es un assistant documentaire rigoureux.
1. Appuie tes réponses exclusivement sur les extraits fournis.
2. Si l'information est absente, réponds exactement : « Les documents fournis ne permettent pas de répondre à cette question. »
3. Fais suivre chaque affirmation de sa source au format [doc_N].
4. Si la couverture est partielle, réponds sur la partie couverte et précise ce qui manque.
5. Réponds en français, en trois phrases au maximum, puis liste les sources utilisées."""


def construire_entree(contexte: str, question: str) -> str:
    return f"EXTRAITS :\n{contexte}\n\nQUESTION : {question}\n\nRÉPONSE :"


def repondre(question: str, passages: list[Passage], *, client=None, model: str | None = None) -> str:
    return generer(
        SYSTEME,
        construire_entree(formater_simple(passages), question),
        client=client,
        model=model,
    )


if __name__ == "__main__":
    exemple = [Passage("La garantie couvre 24 mois.", {"source": "cgv.pdf", "page": 8})]
    if openai_configure():
        print(repondre("Quelle est la durée de la garantie ?", exemple))
    else:
        print(construire_entree(formater_simple(exemple), "Quelle est la durée de la garantie ?"))
