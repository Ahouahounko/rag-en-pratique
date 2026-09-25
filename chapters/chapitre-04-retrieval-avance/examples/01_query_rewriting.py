"""Query Rewriting avec la Responses API d'OpenAI."""

import os
from typing import Any

INSTRUCTIONS = """Tu reformules des questions pour un moteur documentaire.
- Remplace les pronoms et références implicites grâce à l'historique.
- Rends la question autonome.
- Conserve l'intention exacte.
- Ne réponds jamais à la question.
Retourne uniquement la question reformulée."""


def client_openai() -> Any:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
    from openai import OpenAI

    return OpenAI()


def reecrire_requete(
    question: str,
    historique: list[str] | None = None,
    *,
    client: Any = None,
    model: str | None = None,
) -> str:
    """Rend une question autonome en utilisant au plus trois tours récents."""

    derniers = (historique or [])[-3:]
    bloc = "\n".join(f"- {tour}" for tour in derniers) or "Aucun historique."
    response = (client or client_openai()).responses.create(
        model=model or os.getenv("OPENAI_MODEL"),
        instructions=INSTRUCTIONS,
        input=f"Historique :\n{bloc}\n\nQuestion originale : {question}",
    )
    return response.output_text.strip()


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple facultatif : configurez OPENAI_API_KEY et OPENAI_MODEL.")
    else:
        tours = ["Nous examinons les conditions de livraison d'une commande en ligne."]
        print(reecrire_requete("Et pour les délais ?", tours))
