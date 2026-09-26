"""Cache sémantique avec expiration, éviction LRU et statistiques."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


@dataclass
class Entree:
    vecteur: np.ndarray
    reponse: object
    cree_a: float
    dernier_acces: float
    nb_acces: int = 0


class CacheSemantique:
    def __init__(
        self,
        encodeur,
        *,
        seuil: float = 0.95,
        duree_vie: float = 3_600,
        taille_max: int = 1_000,
        horloge: Callable[[], float] = time.time,
    ) -> None:
        if not 0 <= seuil <= 1:
            raise ValueError("seuil doit être compris entre 0 et 1")
        if duree_vie <= 0 or taille_max <= 0:
            raise ValueError("duree_vie et taille_max doivent être strictement positifs")
        self.encodeur = encodeur
        self.seuil = seuil
        self.duree_vie = duree_vie
        self.taille_max = taille_max
        self.horloge = horloge
        self.entrees: dict[str, Entree] = {}
        self.stats = {"succes": 0, "echecs": 0}

    def chercher(self, question: str):
        self._purger()
        if not self.entrees:
            self.stats["echecs"] += 1
            return None

        vecteur = self._encoder(question)
        cles = list(self.entrees)
        matrice = np.vstack([self.entrees[cle].vecteur for cle in cles])
        similarites = matrice @ vecteur
        meilleur = int(np.argmax(similarites))
        if float(similarites[meilleur]) < self.seuil:
            self.stats["echecs"] += 1
            return None

        entree = self.entrees[cles[meilleur]]
        entree.dernier_acces = self.horloge()
        entree.nb_acces += 1
        self.stats["succes"] += 1
        return entree.reponse

    def enregistrer(self, question: str, reponse: object) -> None:
        self._purger()
        if question not in self.entrees and len(self.entrees) >= self.taille_max:
            self._evincer()
        maintenant = self.horloge()
        self.entrees[question] = Entree(
            vecteur=self._encoder(question),
            reponse=reponse,
            cree_a=maintenant,
            dernier_acces=maintenant,
        )

    def taux_de_succes(self) -> float:
        total = self.stats["succes"] + self.stats["echecs"]
        return self.stats["succes"] / total if total else 0.0

    def _encoder(self, texte: str) -> np.ndarray:
        if hasattr(self.encodeur, "embed"):
            brut = self.encodeur.embed([texte])[0]
        else:
            brut = self.encodeur.encode(texte)
        vecteur = np.asarray(brut, dtype=float)
        norme = np.linalg.norm(vecteur)
        if not norme:
            raise ValueError("L'encodeur a produit un vecteur nul")
        return vecteur / norme

    def _purger(self) -> None:
        limite = self.horloge() - self.duree_vie
        for cle in [cle for cle, entree in self.entrees.items() if entree.cree_a < limite]:
            del self.entrees[cle]

    def _evincer(self) -> None:
        cle = min(self.entrees, key=lambda item: self.entrees[item].dernier_acces)
        del self.entrees[cle]


if __name__ == "__main__":
    class EncodeurDemo:
        def encode(self, texte: str) -> list[float]:
            return [float("retour" in texte.lower()), 0.1]

    cache = CacheSemantique(EncodeurDemo(), seuil=0.9)
    cache.enregistrer("Quel est le délai de retour ?", "30 jours")
    print(cache.chercher("Quel est le délai de retour ?"), cache.taux_de_succes())
