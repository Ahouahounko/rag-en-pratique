# src/retrieval/retriever.py
import logging
from dataclasses import dataclass

from FlagEmbedding import BGEM3FlagModel
from qdrant_client import QdrantClient
from qdrant_client.models import (
    FieldCondition, Filter, MatchValue, NamedSparseVector,
    NamedVector, SearchRequest, SparseVector,
)
from sentence_transformers import CrossEncoder

from src.config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class Passage:
    """Un chunk recupere, avec toute sa tracabilite."""
    texte: str
    source: str
    page: int
    departement: str
    score_dense: float = 0.0
    score_rerank: float = 0.0
    chunk_id: int = 0


class RetrieverHybride:
    """Dense + sparse, fusionnes par les rangs, puis reclasses."""

    def __init__(self):
        config = get_settings()
        self.client = QdrantClient(url=config.qdrant_url)
        self.collection = config.qdrant_collection
        self.k_initial = config.retrieval_initial_k
        self.k_final = config.retrieval_final_k
        self.seuil_dense = config.retrieval_score_threshold
        self.seuil_rerank = config.rerank_score_threshold
        self.hybride = config.use_hybrid_search
        self.reclasser = config.use_reranking

        # IMPERATIF : le meme modele qu'a l'ingestion. Un modele
        # different projette dans un autre espace ; les distances
        # calculees n'auraient aucun sens, sans aucune erreur levee.
        self.encodeur = BGEM3FlagModel(config.embedding_model,
                                       use_fp16=True)

        self.reclasseur = None
        if self.reclasser:
            try:
                self.reclasseur = CrossEncoder(config.reranker_model)
            except Exception as erreur:
                # Degradation gracieuse : sans re-ranker, on sert
                # quand meme, avec le classement dense.
                logger.error("Re-ranker indisponible : %s", erreur)

    def chercher(self, question: str,
                 filtres: dict = None) -> list[Passage]:
        """Encodage -> recherche -> fusion -> reclassement."""
        sortie = self.encodeur.encode(
            [question], return_dense=True,
            return_sparse=True, return_colbert_vecs=False,
        )
        dense = sortie["dense_vecs"][0].tolist()
        epars = sortie["lexical_weights"][0]

        filtre = self._filtre(filtres)

        if self.hybride:
            resultats = self.client.search_batch(
                collection_name=self.collection,
                requests=[
                    SearchRequest(
                        vector=NamedVector(name="", vector=dense),
                        filter=filtre, limit=self.k_initial,
                        with_payload=True,
                        score_threshold=self.seuil_dense,
                    ),
                    SearchRequest(
                        vector=NamedSparseVector(
                            name="sparse",
                            vector=SparseVector(
                                indices=list(epars.keys()),
                                values=list(epars.values()),
                            ),
                        ),
                        filter=filtre, limit=self.k_initial,
                        with_payload=True,
                    ),
                ],
            )
            passages = self._fusionner(resultats[0], resultats[1])
        else:
            bruts = self.client.search(
                collection_name=self.collection,
                query_vector=dense, query_filter=filtre,
                limit=self.k_initial, with_payload=True,
                score_threshold=self.seuil_dense,
            )
            passages = [self._convertir(r) for r in bruts]

        if not passages:
            # Cas frequent avec un filtre selectif : on le journalise
            # explicitement, sinon on cherchera la cause ailleurs.
            logger.warning("Aucun passage | question=%r filtres=%r",
                           question[:80], filtres)
            return []

        if self.reclasseur and len(passages) > 1:
            passages = self._reclasser(question, passages)

        return passages[:self.k_final]

    # ---------- internes ----------

    def _fusionner(self, dense: list, epars: list,
                   k: int = 60) -> list[Passage]:
        """Fusion reciproque des rangs (RRF).

        On ignore volontairement les scores : ceux d'une recherche
        dense et d'une recherche lexicale ne sont pas comparables.
        Seul le rang l'est.
        """
        cumul = {}
        for liste in (dense, epars):
            for rang, resultat in enumerate(liste, start=1):
                cle = resultat.id
                if cle not in cumul:
                    cumul[cle] = {"passage": self._convertir(resultat),
                                  "score": 0.0}
                cumul[cle]["score"] += 1.0 / (k + rang)

        ordonnes = sorted(cumul.values(),
                          key=lambda e: e["score"], reverse=True)
        return [e["passage"] for e in ordonnes]

    def _reclasser(self, question: str,
                   passages: list[Passage]) -> list[Passage]:
        """Cross-encoder, puis filtrage par seuil.

        Le filtrage autorise le systeme a ne rien renvoyer : mieux
        vaut une abstention qu'un contexte hors sujet.
        """
        try:
            paires = [(question, p.texte) for p in passages]
            for passage, score in zip(passages,
                                      self.reclasseur.predict(paires)):
                passage.score_rerank = float(score)
        except Exception as erreur:
            logger.error("Reclassement echoue, repli dense : %s", erreur)
            return passages

        retenus = [p for p in passages
                   if p.score_rerank >= self.seuil_rerank]
        retenus.sort(key=lambda p: p.score_rerank, reverse=True)
        return retenus

    def _convertir(self, resultat) -> Passage:
        charge = resultat.payload
        return Passage(
            texte=charge["texte"],
            source=charge.get("source", ""),
            page=charge.get("page", 0),
            departement=charge.get("departement", ""),
            score_dense=resultat.score,
            chunk_id=charge.get("chunk_id", 0),
        )

    def _filtre(self, filtres: dict):
        if not filtres:
            return None
        conditions = [
            FieldCondition(key=cle, match=MatchValue(value=valeur))
            for cle, valeur in filtres.items() if valeur
        ]
        return Filter(must=conditions) if conditions else None
