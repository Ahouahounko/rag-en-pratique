"""Sélectionner les passages qui tiennent dans un budget de tokens."""

from __future__ import annotations

from dataclasses import replace

import tiktoken

from rag_en_pratique.prompting import Passage


class BudgetContexte:
    def __init__(
        self,
        modele: str = "gpt-4o",
        fenetre: int = 8000,
        reserve_reponse: int = 1000,
        minimum_utile: int = 150,
    ) -> None:
        try:
            self.encodeur = tiktoken.encoding_for_model(modele)
        except KeyError:
            self.encodeur = tiktoken.get_encoding("cl100k_base")
        self.fenetre = fenetre
        self.reserve_reponse = reserve_reponse
        self.minimum_utile = minimum_utile

    def compter(self, texte: str) -> int:
        return len(self.encodeur.encode(texte))

    def ajuster(self, passages: list[Passage], systeme: str, question: str) -> list[Passage]:
        fixe = self.compter(systeme) + self.compter(question) + self.reserve_reponse + 200
        disponible = self.fenetre - fixe
        if disponible <= 0:
            raise ValueError("Instructions et question saturent déjà la fenêtre")
        retenus: list[Passage] = []
        consomme = 0
        for passage in passages:
            jetons = self.encodeur.encode(passage.page_content)
            if consomme + len(jetons) <= disponible:
                retenus.append(passage)
                consomme += len(jetons)
                continue
            reste = disponible - consomme
            if reste >= self.minimum_utile:
                texte = self.encodeur.decode(jetons[:reste]) + " […extrait tronqué]"
                retenus.append(replace(passage, page_content=texte))
            break
        return retenus


if __name__ == "__main__":
    budget = BudgetContexte(fenetre=400, reserve_reponse=50, minimum_utile=10)
    passages = [Passage("information utile " * 80), Passage("second passage " * 80)]
    print([budget.compter(p.page_content) for p in budget.ajuster(passages, "système", "question")])
