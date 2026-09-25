"""Utilitaires partagés par les exemples d'observabilité du chapitre 8."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PassageEvaluation:
    id: str
    texte: str
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def extraire_json(texte: str) -> dict[str, Any]:
    nettoye = texte.strip().removeprefix("```json").removesuffix("```").strip()
    debut, fin = nettoye.find("{"), nettoye.rfind("}")
    if debut < 0 or fin < debut:
        raise ValueError("Aucun objet JSON trouvé")
    valeur = json.loads(nettoye[debut : fin + 1])
    if not isinstance(valeur, dict):
        raise TypeError("Un objet JSON était attendu")
    return valeur


def extraire_note(texte: str) -> int:
    resultat = re.search(r"\bnote\s*:\s*([1-5])\b", texte, re.IGNORECASE)
    if not resultat:
        raise ValueError(f"Note 1-5 introuvable dans {texte!r}")
    return int(resultat.group(1))


PROMPT_JUGE_FAITHFULNESS = """Tu es un évaluateur impartial.
Évalue uniquement la fidélité au contexte, pas le style ni la vérité générale.
Pour chaque affirmation de la réponse, indique le fragment qui l'étaye ou « aucun ».
Termine exactement par deux sections :
JUSTIFICATION : synthèse vérifiable de ton contrôle
NOTE : entier de 1 à 5
1 signifie majoritairement inventé ; 5 signifie entièrement étayé.

PASSAGES :
{contexte}

QUESTION : {question}

RÉPONSE À ÉVALUER :
{reponse}"""
