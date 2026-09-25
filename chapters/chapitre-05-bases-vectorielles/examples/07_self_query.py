"""Transformer une question en requête sémantique et filtres structurés."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequeteStructuree:
    texte: str
    filtres: dict[str, str]


SCHEMA = {
    "departement": ["RH", "juridique", "finance", "produit", "IT"],
    "confidentialite": ["public", "interne", "confidentiel"],
    "date_minimale": "AAAA-MM-JJ",
}


def construire_self_query(
    question: str,
    *,
    client: Any | None = None,
    model: str | None = None,
) -> RequeteStructuree:
    """Demande à OpenAI un JSON séparant recherche sémantique et filtres."""
    if client is None:
        from openai import OpenAI

        client = OpenAI()
    model = model or os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Définissez OPENAI_MODEL.")
    reponse = client.responses.create(
        model=model,
        input=(
            "Retourne uniquement un objet JSON avec les clés texte et filtres. "
            f"Filtres autorisés : {json.dumps(SCHEMA, ensure_ascii=False)}. "
            f"Question : {question}"
        ),
    )
    donnees = json.loads(reponse.output_text)
    filtres = {cle: str(valeur) for cle, valeur in donnees.get("filtres", {}).items()}
    inconnus = set(filtres) - set(SCHEMA)
    if inconnus:
        raise ValueError(f"Filtres non autorisés : {sorted(inconnus)}")
    return RequeteStructuree(str(donnees["texte"]), filtres)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple prêt : définissez OPENAI_API_KEY et OPENAI_MODEL.")
    else:
        print(construire_self_query("Contrats juridiques publiés depuis 2025"))
