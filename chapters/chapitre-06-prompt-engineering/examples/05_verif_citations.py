"""Vérifier la présence et la validité formelle des citations."""

from __future__ import annotations

import re

from rag_en_pratique.prompting import Passage


def verifier_citations(reponse: str, passages: list[Passage]) -> dict[str, object]:
    cites = set(re.findall(r"\[doc_(\d+)\]", reponse))
    disponibles = {str(i) for i in range(1, len(passages) + 1)}
    phrases = [
        phrase.strip()
        for phrase in re.split(r"(?<=[.!?])\s+", reponse)
        if len(phrase.strip()) > 30
    ]
    formule_refus = "ne permettent pas de répondre"
    sans_source = [
        phrase
        for phrase in phrases
        if "[doc_" not in phrase and formule_refus not in phrase.lower()
    ]
    inventees = cites - disponibles
    return {
        "citations_inventees": sorted(inventees),
        "extraits_non_cites": sorted(disponibles - cites),
        "phrases_sans_source": sans_source,
        "conforme": not inventees and not sans_source,
    }


if __name__ == "__main__":
    passages = [Passage("Garantie 24 mois.")]
    print(verifier_citations("La garantie dure 24 mois [doc_1].", passages))
