"""Construire et interroger un index FAISS HNSW."""

from __future__ import annotations

import numpy as np


def construire_index_hnsw(
    vecteurs: np.ndarray,
    dimension: int,
    m: int = 32,
    ef_construction: int = 200,
):
    """Crée un index HNSW utilisant le produit scalaire sur des vecteurs normalisés."""
    import faiss

    donnees = np.asarray(vecteurs, dtype=np.float32).copy()
    if donnees.ndim != 2 or donnees.shape[1] != dimension:
        raise ValueError(f"Forme attendue : (n, {dimension})")
    faiss.normalize_L2(donnees)
    index = faiss.IndexHNSWFlat(dimension, m, faiss.METRIC_INNER_PRODUCT)
    index.hnsw.efConstruction = ef_construction
    index.add(donnees)
    return index


def chercher(index, vecteur_requete: np.ndarray, k: int = 5, ef_search: int = 64):
    """Renvoie les scores cosinus et les positions des voisins."""
    import faiss

    index.hnsw.efSearch = ef_search
    requete = np.asarray(vecteur_requete, dtype=np.float32).reshape(1, -1).copy()
    faiss.normalize_L2(requete)
    scores, positions = index.search(requete, k)
    return scores[0], positions[0]


if __name__ == "__main__":
    corpus = np.array([[1, 0, 0], [0.9, 0.1, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
    hnsw = construire_index_hnsw(corpus, dimension=3, m=8)
    scores, ids = chercher(hnsw, np.array([1, 0, 0]), k=2)
    print(list(zip(ids.tolist(), scores.round(3).tolist(), strict=True)))
