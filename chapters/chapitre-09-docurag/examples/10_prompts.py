"""Gabarits versionnés de DocuRAG."""

VERSION_PROMPT = "1.2"

SYSTEME = """Tu es {app_name}, un assistant documentaire rigoureux.

1. Tu réponds EXCLUSIVEMENT à partir des extraits fournis.
2. Si l'information ne s'y trouve pas, écris exactement :
   "Cette information ne figure pas dans les documents consultés."
3. Fais suivre chaque affirmation de sa source : [doc_N].
4. Si les extraits ne couvrent qu'une partie de la question, précise ce qui manque.
5. Réponds en français, de manière concise et professionnelle.

Toute affirmation doit pouvoir être reliée à un extrait."""

UTILISATEUR = """EXTRAITS :
{contexte}

QUESTION : {question}

RÉPONSE :"""


def construire_prompt(app_name: str, contexte: str, question: str) -> tuple[str, str]:
    return SYSTEME.format(app_name=app_name), UTILISATEUR.format(
        contexte=contexte,
        question=question,
    )


if __name__ == "__main__":
    systeme, utilisateur = construire_prompt(
        "DocuRAG",
        "[doc_1] retours.md\nLes retours sont acceptés sous 30 jours.",
        "Quel est le délai de retour ?",
    )
    print(systeme, utilisateur, sep="\n\n")
