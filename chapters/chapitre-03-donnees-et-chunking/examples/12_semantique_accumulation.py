"""Détection de rupture sémantique par accumulation."""

import re
from collections import Counter

import numpy as np


def vectoriser(texte: str, vocabulaire: list[str]) -> np.ndarray:
    compte = Counter(re.findall(r"\w+", texte.lower()))
    return np.array([compte[mot] for mot in vocabulaire], dtype=float)


def cosinus(gauche: np.ndarray, droite: np.ndarray) -> float:
    denominateur = np.linalg.norm(gauche) * np.linalg.norm(droite)
    return float(np.dot(gauche, droite) / denominateur) if denominateur else 0.0


def chunking_par_accumulation(segments: list[str], seuil: float = 0.15) -> list[str]:
    if not segments:
        return []
    vocabulaire = sorted({mot for segment in segments for mot in re.findall(r"\w+", segment.lower())})
    chunk_courant = [segments[0]]
    vecteurs_courants = [vectoriser(segments[0], vocabulaire)]
    chunks: list[str] = []
    for segment in segments[1:]:
        vecteur = vectoriser(segment, vocabulaire)
        vecteur_reference = np.mean(vecteurs_courants, axis=0)
        if cosinus(vecteur_reference, vecteur) >= seuil:
            chunk_courant.append(segment)
            vecteurs_courants.append(vecteur)
        else:
            chunks.append(" ".join(chunk_courant))
            chunk_courant = [segment]
            vecteurs_courants = [vecteur]
    chunks.append(" ".join(chunk_courant))
    return chunks


if __name__ == "__main__":
    segments = [
        "Le retour produit reste possible trente jours.",
        "Le remboursement du produit suit le retour.",
        "La livraison express utilise un transporteur.",
    ]
    print(chunking_par_accumulation(segments))
