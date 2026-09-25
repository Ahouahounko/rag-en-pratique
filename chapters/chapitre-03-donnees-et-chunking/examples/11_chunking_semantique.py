"""Chunking sémantique avec un modèle TF-IDF local et explicable."""

import math
import re
from collections import Counter

import numpy as np


class ModeleTFIDF:
    """Petit modèle d'embedding lexical, sans service ni clé API."""

    def embed_documents(self, textes: list[str]) -> list[list[float]]:
        mots = [re.findall(r"\w+", texte.lower()) for texte in textes]
        vocabulaire = sorted({mot for document in mots for mot in document})
        frequences_documents = Counter(mot for mot in vocabulaire for doc in mots if mot in doc)
        vecteurs: list[list[float]] = []
        for document in mots:
            occurrences = Counter(document)
            vecteurs.append(
                [
                    occurrences[mot] * math.log((1 + len(mots)) / (1 + frequences_documents[mot]))
                    for mot in vocabulaire
                ]
            )
        return vecteurs


def chunking_semantique(
    texte: str,
    modele_embedding: ModeleTFIDF,
    percentile: int = 75,
) -> list[str]:
    phrases = [phrase.strip() for phrase in re.split(r"(?<=[.!?])\s+", texte) if phrase.strip()]
    if len(phrases) < 2:
        return [texte]
    vecteurs = np.array(modele_embedding.embed_documents(phrases), dtype=float)
    normes = np.linalg.norm(vecteurs, axis=1, keepdims=True) + 1e-8
    unitaires = vecteurs / normes
    distances = 1.0 - np.sum(unitaires[1:] * unitaires[:-1], axis=1)
    seuil = float(np.percentile(distances, percentile))

    chunks: list[str] = []
    courant = [phrases[0]]
    for index, distance in enumerate(distances, start=1):
        if distance >= seuil:
            chunks.append(" ".join(courant))
            courant = [phrases[index]]
        else:
            courant.append(phrases[index])
    chunks.append(" ".join(courant))
    return chunks


if __name__ == "__main__":
    texte = (
        "Les retours sont acceptés pendant trente jours. "
        "Un remboursement est alors déclenché. "
        "La livraison express arrive demain. "
        "Le transporteur fournit un numéro de suivi."
    )
    for index, chunk in enumerate(chunking_semantique(texte, ModeleTFIDF()), start=1):
        print(index, chunk)
