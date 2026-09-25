import faiss
import numpy as np


def construire_index_ivf(vecteurs: np.ndarray,
                         dimension: int,
                         n_list: int = None) -> faiss.Index:
    """Index IVF, adapte aux corpus de 10M a 100M vecteurs."""

    n = len(vecteurs)
    if n_list is None:
        n_list = int(np.sqrt(n))         # regle empirique usuelle

    donnees = vecteurs.astype(np.float32).copy()
    faiss.normalize_L2(donnees)

    # 1. Structure : un quantifieur plat sert a comparer aux centroides
    quantifieur = faiss.IndexFlatIP(dimension)
    index = faiss.IndexIVFFlat(quantifieur, dimension, n_list,
                               faiss.METRIC_INNER_PRODUCT)

    # 2. Entrainement : c'est ICI que les frontieres sont apprises.
    #    L'echantillon doit representer TOUT le corpus.
    echantillon = donnees
    if n > 500_000:
        tirage = np.random.choice(n, 500_000, replace=False)
        echantillon = donnees[tirage]

    index.train(echantillon)

    # 3. Remplissage
    index.add(donnees)

    # Curseur de qualite, ajustable a chaud comme ef_search
    index.nprobe = max(1, n_list // 10)

    return index
