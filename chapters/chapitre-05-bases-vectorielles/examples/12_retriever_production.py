"""Pipeline de retrieval filtré, reclassé, journalisé et résilient."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

journal = logging.getLogger(__name__)


@dataclass
class Passage:
    texte: str
    source: str
    page: int
    score_dense: float = 0.0
    score_reclassement: float = 0.0
    metadonnees: dict[str, Any] = field(default_factory=dict)


class RetrieverProduction:
    def __init__(
        self,
        client,
        collection: str,
        encodeur,
        reclasseur=None,
        n_candidats: int = 20,
        n_final: int = 5,
        seuil_reclassement: float = 0.0,
    ) -> None:
        self.client = client
        self.collection = collection
        self.encodeur = encodeur
        self.reclasseur = reclasseur
        self.n_candidats = n_candidats
        self.n_final = n_final
        self.seuil = seuil_reclassement

    @classmethod
    def depuis_modeles(
        cls,
        url_qdrant: str,
        collection: str,
        modele_embedding: str,
        modele_reclassement: str = "cross-encoder/ms-marco-MiniLM-L6-v2",
    ) -> RetrieverProduction:
        from qdrant_client import QdrantClient
        from sentence_transformers import CrossEncoder, SentenceTransformer

        encodeur = SentenceTransformer(modele_embedding)
        try:
            reclasseur = CrossEncoder(modele_reclassement)
        except Exception as erreur:  # noqa: BLE001 - repli de disponibilité volontaire
            journal.warning("Reclasseur indisponible : %s", erreur)
            reclasseur = None
        return cls(QdrantClient(url=url_qdrant), collection, encodeur, reclasseur)

    def chercher(self, question: str, filtres: dict[str, object] | None = None) -> list[Passage]:
        depart = time.perf_counter()
        vecteur = self.encodeur.encode(question, normalize_embeddings=True).tolist()
        resultat = self.client.query_points(
            collection_name=self.collection,
            query=vecteur,
            query_filter=self._filtre(filtres),
            limit=self.n_candidats,
            with_payload=True,
            score_threshold=0.3,
        )
        passages = [
            Passage(
                texte=point.payload["texte"],
                source=point.payload.get("source", ""),
                page=point.payload.get("page", 0),
                score_dense=point.score,
                metadonnees=point.payload,
            )
            for point in resultat.points
        ]
        passages = self._reclasser(question, passages)
        journal.info(
            "retrieval | duree=%.0fms | candidats=%d | retenus=%d",
            (time.perf_counter() - depart) * 1000,
            len(resultat.points),
            min(len(passages), self.n_final),
        )
        return passages[: self.n_final]

    def _reclasser(self, question: str, passages: list[Passage]) -> list[Passage]:
        if self.reclasseur is None or len(passages) <= 1:
            return passages
        try:
            paires = [(question, passage.texte) for passage in passages]
            for passage, score in zip(passages, self.reclasseur.predict(paires), strict=True):
                passage.score_reclassement = float(score)
            retenus = [p for p in passages if p.score_reclassement >= self.seuil]
            return sorted(retenus, key=lambda p: p.score_reclassement, reverse=True)
        except Exception as erreur:  # noqa: BLE001 - repli dense volontaire
            journal.warning("Reclassement échoué, repli dense : %s", erreur)
            return passages

    @staticmethod
    def _filtre(filtres: dict[str, object] | None):
        if not filtres:
            return None
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        return Filter(
            must=[
                FieldCondition(key=cle, match=MatchValue(value=valeur))
                for cle, valeur in filtres.items()
            ]
        )


if __name__ == "__main__":
    print("Injectez un client Qdrant et les modèles, ou utilisez RetrieverProduction.depuis_modeles().")
