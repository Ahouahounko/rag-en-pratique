"""Construire un index FAISS IVF et régler son compromis rappel/latence."""

from __future__ import annotations

import numpy as np


def construire_index_ivf(
    vecteurs: np.ndarray,
    dimension: int,
    n_list: int | None = None,
    graine: int = 42,
):
    import faiss

    donnees = np.asarray(vecteurs, dtype=np.float32).copy()
    if donnees.ndim != 2 or donnees.shape[1] != dimension:
        raise ValueError(f"Forme attendue : (n, {dimension})")
    n = len(donnees)
    if n < 2:
        raise ValueError("IVF demande au moins deux vecteurs")
    n_list = n_list or max(1, min(int(np.sqrt(n)), n // 2))
    faiss.normalize_L2(donnees)

    quantifieur = faiss.IndexFlatIP(dimension)
    index = faiss.IndexIVFFlat(quantifieur, dimension, n_list, faiss.METRIC_INNER_PRODUCT)
    generateur = np.random.default_rng(graine)
    echantillon = donnees
    if n > 500_000:
        echantillon = donnees[generateur.choice(n, 500_000, replace=False)]
    index.train(echantillon)
    index.add(donnees)
    index.nprobe = max(1, n_list // 10)
    return index


def chercher(index, requete: np.ndarray, k: int = 5, nprobe: int | None = None):
    import faiss

    if nprobe is not None:
        index.nprobe = nprobe
    vecteur = np.asarray(requete, dtype=np.float32).reshape(1, -1).copy()
    faiss.normalize_L2(vecteur)
    return tuple(element[0] for element in index.search(vecteur, k))


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    corpus = rng.normal(size=(200, 8)).astype(np.float32)
    ivf = construire_index_ivf(corpus, dimension=8, n_list=8)
    scores, ids = chercher(ivf, corpus[0], k=3, nprobe=4)
    print(list(zip(ids.tolist(), scores.round(3).tolist(), strict=True)))
