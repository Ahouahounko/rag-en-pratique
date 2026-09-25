"""Ajouter un exemple nominal et un exemple de refus au prompt RAG."""

from __future__ import annotations

from rag_en_pratique.prompting import generer, openai_configure

SYSTEME = "Réponds exclusivement avec les extraits et cite chaque affirmation au format [doc_N]."


def construire_messages(contexte: str, question: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": "EXTRAIT: [doc_1] Garantie 24 mois. QUESTION: Quelle durée ?",
        },
        {"role": "assistant", "content": "La garantie couvre 24 mois [doc_1]."},
        {
            "role": "user",
            "content": "EXTRAIT: [doc_1] Garantie 24 mois. QUESTION: Est-elle transférable ?",
        },
        {
            "role": "assistant",
            "content": "Les documents fournis ne permettent pas de répondre à cette question.",
        },
        {"role": "user", "content": f"EXTRAITS :\n{contexte}\n\nQUESTION : {question}"},
    ]


def repondre_few_shot(
    contexte: str,
    question: str,
    *,
    client=None,
    model: str | None = None,
) -> str:
    return generer(
        SYSTEME,
        construire_messages(contexte, question),
        client=client,
        model=model,
    )


if __name__ == "__main__":
    messages = construire_messages("[doc_1] Retour sous 30 jours.", "Quel délai ?")
    print(repondre_few_shot(messages[-1]["content"], "Quel délai ?") if openai_configure() else messages)
