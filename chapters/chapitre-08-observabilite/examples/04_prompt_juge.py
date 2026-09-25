"""Construire le prompt auditable d'un juge de fidélité."""

from rag_en_pratique.observability import PROMPT_JUGE_FAITHFULNESS


def construire_prompt_juge(contexte: str, question: str, reponse: str) -> str:
    return PROMPT_JUGE_FAITHFULNESS.format(
        contexte=contexte,
        question=question,
        reponse=reponse,
    )


if __name__ == "__main__":
    print(construire_prompt_juge("Garantie 24 mois.", "Quelle durée ?", "24 mois."))
