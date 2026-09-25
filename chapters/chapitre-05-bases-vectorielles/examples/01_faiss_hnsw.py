import faiss
import numpy as np


def construire_index_hnsw(vecteurs: np.ndarray,
                          dimension: int,
                          M: int = 32,
                          ef_construction: int = 200) -> faiss.Index:
    """Index HNSW pour un corpus allant jusqu'a ~10M vecteurs.

    M=32 est plus genereux que le defaut (16) : meilleur recall,
    environ 50 % de memoire en plus. Bon compromis en RAG.
    """
    index = faiss.IndexHNSWFlat(dimension, M)
    index.hnsw.efConstruction = ef_construction

    # FAISS raisonne en DISTANCES, pas en similarites.
    # Normaliser les vecteurs rend la distance euclidienne
    # equivalente a la similarite cosinus. Oublier cette ligne
    # est l'erreur la plus frequente avec FAISS.
    donnees = vecteurs.astype(np.float32).copy()
    faiss.normalize_L2(donnees)

    index.add(donnees)
    return index


def chercher(index: faiss.Index, vecteur_requete: np.ndarray,
             k: int = 5, ef_search: int = 64) -> tuple:
    """Recherche des k plus proches voisins.

    ef_search est le curseur recall/latence, ajustable a chaud :
        32  -> plus rapide, moins precis
        64  -> valeur de depart raisonnable
        128 -> plus precis, plus lent
    """
    index.hnsw.efSearch = ef_search

    requete = vecteur_requete.astype(np.float32).reshape(1, -1).copy()
    faiss.normalize_L2(requete)          # meme traitement qu'a l'indexation

    distances, positions = index.search(requete, k)
    return distances[0], positions[0]
