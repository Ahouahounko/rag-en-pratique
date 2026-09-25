# src/ingestion/indexer.py
import logging
import uuid

from FlagEmbedding import BGEM3FlagModel
from langchain.schema import Document
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, HnswConfigDiff, PointStruct,
    SparseVectorParams, VectorParams,
)
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import get_settings

logger = logging.getLogger(__name__)


class Indexeur:
    """Vectorise les chunks et les ecrit dans Qdrant.

    bge-m3 produit dense ET sparse en un seul passage : les deux
    representations vivent dans le meme point Qdrant, donc rien
    a synchroniser entre deux index.
    """

    def __init__(self):
        config = get_settings()
        self.client = QdrantClient(url=config.qdrant_url)
        self.collection = config.qdrant_collection

        logger.info("Chargement du modele %s...", config.embedding_model)
        self.modele = BGEM3FlagModel(
            config.embedding_model,
            use_fp16=True,        # moitie moins de memoire, qualite stable
        )

    def preparer_collection(self, dimension: int = 1024,
                            recreer: bool = False) -> None:
        """Cree la collection avec support dense + sparse."""
        existantes = [c.name for c in
                      self.client.get_collections().collections]

        if self.collection in existantes:
            if not recreer:
                logger.info("Collection existante, conservee.")
                return
            self.client.delete_collection(self.collection)
            logger.warning("Collection supprimee et recreee.")

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=dimension,
                distance=Distance.COSINE,
                # m=32 plutot que 16 : meilleur rappel, memoire en
                # hausse d'environ 50 %. Cf. chapitre sur les bases
                # vectorielles.
                hnsw_config=HnswConfigDiff(m=32, ef_construct=200),
            ),
            sparse_vectors_config={"sparse": SparseVectorParams()},
        )
        logger.info("Collection creee (dimension %d).", dimension)

    @retry(stop=stop_after_attempt(3),
           wait=wait_exponential(multiplier=2, min=2, max=30))
    def _ecrire(self, points: list[PointStruct]) -> None:
        """Ecriture d'un lot, avec trois tentatives espacees.

        Sans cette reprise, un incident reseau de deux secondes
        fait perdre vingt minutes d'ingestion.
        """
        self.client.upsert(collection_name=self.collection,
                           points=points)

    def indexer(self, chunks: list[Document],
                taille_lot: int = 32) -> int:
        """Encode et ecrit les chunks par lots."""
        total = 0
        nb_lots = (len(chunks) + taille_lot - 1) // taille_lot

        for numero in range(nb_lots):
            lot = chunks[numero * taille_lot:(numero + 1) * taille_lot]

            sorties = self.modele.encode(
                [c.page_content for c in lot],
                return_dense=True,
                return_sparse=True,
                return_colbert_vecs=False,
            )

            points = []
            for chunk, dense, epars in zip(lot,
                                           sorties["dense_vecs"],
                                           sorties["lexical_weights"]):
                points.append(PointStruct(
                    id=str(uuid.uuid4()),
                    vector={
                        "": dense.tolist(),
                        "sparse": {
                            "indices": list(epars.keys()),
                            "values": list(epars.values()),
                        },
                    },
                    payload={
                        "texte": chunk.page_content,
                        "source": chunk.metadata.get("source", ""),
                        "page": chunk.metadata.get("page", 0),
                        "departement": chunk.metadata.get("departement", ""),
                        "empreinte": chunk.metadata.get("empreinte", ""),
                        "chunk_id": chunk.metadata.get("chunk_id", 0),
                    },
                ))

            self._ecrire(points)
            total += len(lot)
            logger.info("Lot %d/%d (%d/%d chunks)",
                        numero + 1, nb_lots, total, len(chunks))

        return total
