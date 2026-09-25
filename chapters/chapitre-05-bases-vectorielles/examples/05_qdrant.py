"""Configurer une collection Qdrant dense et sparse."""

from __future__ import annotations


def creer_collection(client, nom: str, dimension: int = 768) -> None:
    from qdrant_client.models import (
        Distance,
        HnswConfigDiff,
        OptimizersConfigDiff,
        SparseIndexParams,
        SparseVectorParams,
        VectorParams,
    )

    client.create_collection(
        collection_name=nom,
        vectors_config=VectorParams(
            size=dimension,
            distance=Distance.COSINE,
            hnsw_config=HnswConfigDiff(
                m=32,
                ef_construct=200,
                full_scan_threshold=10_000,
            ),
        ),
        sparse_vectors_config={
            "lexical": SparseVectorParams(index=SparseIndexParams(on_disk=False))
        },
        optimizers_config=OptimizersConfigDiff(
            indexing_threshold=20_000,
            memmap_threshold=50_000,
        ),
    )


if __name__ == "__main__":
    from qdrant_client import QdrantClient

    qdrant = QdrantClient(":memory:")
    creer_collection(qdrant, "demo", dimension=3)
    print(qdrant.get_collection("demo").status)
