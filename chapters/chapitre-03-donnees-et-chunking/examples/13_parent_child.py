"""Indexation Parent-Child locale et exécutable."""

import math
import re
import uuid
from collections import Counter
from dataclasses import dataclass


def decoupage_mots(texte: str, taille: int, overlap: int) -> list[str]:
    mots = texte.split()
    pas = taille - overlap
    return [" ".join(mots[debut : debut + taille]) for debut in range(0, len(mots), pas)]


def similarite_lexicale(gauche: str, droite: str) -> float:
    mots_gauche = Counter(re.findall(r"\w+", gauche.lower()))
    mots_droite = Counter(re.findall(r"\w+", droite.lower()))
    commun = set(mots_gauche) | set(mots_droite)
    produit = sum(mots_gauche[mot] * mots_droite[mot] for mot in commun)
    norme_gauche = math.sqrt(sum(valeur**2 for valeur in mots_gauche.values()))
    norme_droite = math.sqrt(sum(valeur**2 for valeur in mots_droite.values()))
    return produit / (norme_gauche * norme_droite) if norme_gauche and norme_droite else 0.0


@dataclass(frozen=True)
class Enfant:
    texte: str
    id_parent: str


class MagasinEnfants:
    def __init__(self) -> None:
        self.enfants: list[Enfant] = []

    def ajouter(self, texte: str, id_parent: str) -> None:
        self.enfants.append(Enfant(texte, id_parent))

    def recherche(self, requete: str, k: int = 8) -> list[Enfant]:
        return sorted(
            self.enfants,
            key=lambda enfant: similarite_lexicale(requete, enfant.texte),
            reverse=True,
        )[:k]


def indexer_parent_child(document: str, vector_store: MagasinEnfants, docstore: dict[str, str]) -> None:
    for parent_texte in decoupage_mots(document, taille=50, overlap=10):
        id_parent = str(uuid.uuid4())
        docstore[id_parent] = parent_texte
        for enfant_texte in decoupage_mots(parent_texte, taille=15, overlap=3):
            vector_store.ajouter(enfant_texte, id_parent)


def recuperer_avec_parents(
    requete: str,
    vector_store: MagasinEnfants,
    docstore: dict[str, str],
    k: int = 3,
) -> list[str]:
    enfants = vector_store.recherche(requete, k=k)
    ids_uniques = list(dict.fromkeys(enfant.id_parent for enfant in enfants))
    return [docstore[identifiant] for identifiant in ids_uniques]


if __name__ == "__main__":
    document = ("Les retours sont acceptés pendant trente jours. " * 10) + (
        "La livraison standard prend cinq jours ouvrés. " * 10
    )
    magasin = MagasinEnfants()
    parents: dict[str, str] = {}
    indexer_parent_child(document, magasin, parents)
    print(recuperer_avec_parents("Quel délai pour un retour ?", magasin, parents)[0])
