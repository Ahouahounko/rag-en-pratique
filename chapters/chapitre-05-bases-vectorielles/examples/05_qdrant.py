from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, HnswConfigDiff,
    OptimizersConfigDiff, SparseVectorParams
)


def creer_collection(client: QdrantClient, nom: str,
                     dimension: int = 768) -> None:
    """Collection prete pour l'exploitation."""
    client.create_collection(
        collection_name=nom,

        vectors_config=VectorParams(
            size=dimension,
            distance=Distance.COSINE,
            hnsw_config=HnswConfigDiff(
                m=32,
                ef_construct=200,
                # En dessous de ce seuil, Qdrant fait du kNN exact :
                # sur un petit volume, c'est plus rapide ET exact.
                full_scan_threshold=10_000,
            ),
        ),

        # Vecteurs epars : l'hybride du chapitre 4, mais dans
        # la meme requete et sans second index a synchroniser.
        sparse_vectors_config={
            "lexical": SparseVectorParams(index={"on_disk": False}),
        },

        optimizers_config=OptimizersConfigDiff(
            indexing_threshold=20_000,   # construction du graphe differee
            memmap_threshold=50_000,     # bascule disque au-dela
        ),
    )
