"""Signaler explicitement les contradictions entre extraits."""

from __future__ import annotations

from rag_en_pratique.prompting import generer, openai_configure

INSTRUCTIONS_CONFLITS = """Tu es un analyste documentaire.
En cas de contradiction :
1. Signale-la dès la première phrase.
2. Expose chaque position avec sa source.
3. Compare les dates de révision et indique que la plus récente prévaut a priori.
4. Sans date permettant de trancher, recommande une vérification officielle.
Ne choisis jamais silencieusement une version."""


def analyser_conflits(
    contexte: str,
    question: str,
    *,
    client=None,
    model: str | None = None,
) -> str:
    return generer(
        INSTRUCTIONS_CONFLITS,
        f"EXTRAITS :\n{contexte}\n\nQUESTION : {question}",
        client=client,
        model=model,
    )


if __name__ == "__main__":
    if openai_configure():
        print(analyser_conflits("[doc_1] 30 jours. [doc_2] 14 jours.", "Quel délai ?"))
    else:
        print(INSTRUCTIONS_CONFLITS)
