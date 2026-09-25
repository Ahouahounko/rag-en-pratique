from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import FAISS

def build_ensemble_retriever(chunks: list,
                             vector_store: FAISS,
                             weights: list = None) -> EnsembleRetriever:
    """
    Construit un retriever hybride BM25 + dense avec fusion RRF.

    Args:
        chunks : Documents textuels (pour l'index BM25)
        vector_store : Index vectoriel (pour le retrieval dense)
        weights : [poids_bm25, poids_dense] - defaut [0.4, 0.6]
                  Ajustez selon votre corpus :
                  - Corpus technique (codes, refs)  : [0.5, 0.5]
                  - Corpus conversationnel          : [0.3, 0.7]
    """
    if weights is None:
        weights = [0.4, 0.6]   # Legere preference pour le dense

    # Retriever BM25 (lexical)
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 5

    # Retriever dense (semantique)
    dense_retriever = vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k": 5}
    )

    # Ensemble avec fusion RRF ponderee
    ensemble = EnsembleRetriever(
        retrievers = [bm25_retriever, dense_retriever],
        weights = weights
    )

    return ensemble
