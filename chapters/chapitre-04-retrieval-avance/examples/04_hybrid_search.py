"""Recherche hybride : classement dense, BM25 et fusion RRF."""

import re
from dataclasses import dataclass

from rank_bm25 import BM25Okapi


@dataclass(frozen=True)
class Passage:
    page_content: str
    source: str


def tokeniser(texte: str) -> list[str]:
    return re.findall(r"[a-zà-ÿ0-9\-]+", texte.lower())


def fusion_rrf(listes: list[list[Passage]], constante: int = 60) -> list[Passage]:
    scores: dict[Passage, float] = {}
    for resultats in listes:
        for rang, passage in enumerate(resultats, start=1):
            scores[passage] = scores.get(passage, 0.0) + 1.0 / (constante + rang)
    return sorted(scores, key=scores.get, reverse=True)  # type: ignore[arg-type]


class RechercheHybride:
    def __init__(self, chunks: list[Passage]) -> None:
        self.chunks = chunks
        self.bm25 = BM25Okapi([tokeniser(chunk.page_content) for chunk in chunks])

    def recherche_dense(self, question: str) -> list[Passage]:
        mots = set(tokeniser(question))
        return sorted(
            self.chunks,
            key=lambda chunk: len(mots & set(tokeniser(chunk.page_content))),
            reverse=True,
        )

    def rechercher(self, question: str, k: int = 5) -> list[Passage]:
        dense = self.recherche_dense(question)
        scores = self.bm25.get_scores(tokeniser(question))
        ordre = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)
        lexical = [self.chunks[index] for index in ordre]
        return fusion_rrf([dense, lexical])[:k]


if __name__ == "__main__":
    corpus = [
        Passage("Le produit SKU-4892 est garanti deux ans.", "catalogue.md"),
        Passage("La garantie standard couvre vingt-quatre mois.", "garantie.md"),
        Passage("La livraison prend cinq jours.", "livraison.md"),
    ]
    print(RechercheHybride(corpus).rechercher("garantie SKU-4892", k=2))
