import time
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Entree:
    vecteur: np.ndarray
    reponse: object
    cree_a: float
    dernier_acces: float
    nb_acces: int = 0


class CacheSemantique:
    """Cache par similarite, avec duree de vie et eviction LRU."""

    def __init__(self, encodeur, seuil: float = 0.95,
                 duree_vie: int = 3600, taille_max: int = 1000):
        # MEME encodeur qu'a l'ingestion et au retrieval : deux
        # modeles differents projettent dans des espaces differents.
        self.encodeur = encodeur
        self.seuil = seuil
        self.duree_vie = duree_vie
        self.taille_max = taille_max
        self.entrees: dict[str, Entree] = {}
        self.stats = {"succes": 0, "echecs": 0}

    def chercher(self, question: str):
        """Retourne la reponse en cache, ou None."""
        self._purger()
        if not self.entrees:
            self.stats["echecs"] += 1
            return None

        vecteur = self._encoder(question)

        cles = list(self.entrees)
        matrice = np.vstack([self.entrees[c].vecteur for c in cles])
        similarites = matrice @ vecteur          # vecteurs normalises

        meilleur = int(np.argmax(similarites))
        if similarites[meilleur] < self.seuil:
            self.stats["echecs"] += 1
            return None

        entree = self.entrees[cles[meilleur]]
        entree.dernier_acces = time.time()
        entree.nb_acces += 1
        self.stats["succes"] += 1
        return entree.reponse

    def enregistrer(self, question: str, reponse) -> None:
        if len(self.entrees) >= self.taille_max:
            self._evincer()
        maintenant = time.time()
        self.entrees[question] = Entree(
            vecteur=self._encoder(question), reponse=reponse,
            cree_a=maintenant, dernier_acces=maintenant,
        )

    def taux_de_succes(self) -> float:
        total = self.stats["succes"] + self.stats["echecs"]
        return self.stats["succes"] / total if total else 0.0

    # ---------- internes ----------

    def _encoder(self, texte: str) -> np.ndarray:
        vecteur = np.asarray(self.encodeur.encode(texte), dtype=float)
        return vecteur / (np.linalg.norm(vecteur) + 1e-12)

    def _purger(self) -> None:
        limite = time.time() - self.duree_vie
        for cle in [c for c, e in self.entrees.items()
                    if e.cree_a < limite]:
            del self.entrees[cle]

    def _evincer(self) -> None:
        """Supprime l'entree la moins recemment utilisee."""
        cle = min(self.entrees, key=lambda c: self.entrees[c].dernier_acces)
        del self.entrees[cle]
