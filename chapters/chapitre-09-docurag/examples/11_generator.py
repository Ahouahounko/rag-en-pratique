"""Génération citée avec abstention et niveau de confiance."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from rag_en_pratique.core import Document, SearchResult
from rag_en_pratique.providers import create_generator

ABSTENTION = "Cette information ne figure pas dans les documents consultés."
PROMPT_VERSION = "1.2"


@dataclass
class Reponse:
    texte: str
    sources: list[dict[str, object]] = field(default_factory=list)
    confiance: str = "Bas"
    version_prompt: str = PROMPT_VERSION


class Generateur:
    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
        *,
        client=None,
    ) -> None:
        self.generator = create_generator(provider, model=model, client=client)

    def repondre(self, question: str, passages: Sequence[SearchResult]) -> Reponse:
        if not passages:
            return Reponse(ABSTENTION)
        meilleur = max(passage.score for passage in passages)
        confiance = "Haut" if meilleur >= 0.7 else "Moyen" if meilleur >= 0.4 else "Bas"
        sources = [
            {
                "document": passage.document.metadata.get("source", "document"),
                "pertinence": round(passage.score, 3),
            }
            for passage in passages
        ]
        return Reponse(
            self.generator.generate(question, passages),
            sources=sources,
            confiance=confiance,
        )


def main() -> None:
    passages = [
        SearchResult(
            Document("La livraison prend trois à cinq jours.", {"source": "livraison.md"}),
            1.0,
        )
    ]
    response = Generateur().repondre("Quel est le délai de livraison ?", passages)
    print(response.texte)
    print(response.sources, response.confiance)


if __name__ == "__main__":
    main()
