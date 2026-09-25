# src/ingestion/__init__.py
import logging

from qdrant_client.models import FieldCondition, Filter, MatchValue

from src.config import get_settings
from .chunker import decouper
from .indexer import Indexeur
from .loader import charger_dossier, charger_urls

logger = logging.getLogger(__name__)


def ingerer(chemin: str = None, urls: list[str] = None,
            tout_reconstruire: bool = False) -> dict:
    """Chargement -> decoupage -> indexation.

    tout_reconstruire=False : seuls les documents nouveaux ou
    modifies sont retraites (comparaison des empreintes).
    tout_reconstruire=True  : la collection est recreee de zero.
    """
    config = get_settings()
    chemin = chemin or config.documents_path

    logger.info("=== INGESTION : debut ===")

    documents = charger_dossier(chemin)
    if urls:
        documents.extend(charger_urls(urls))

    indexeur = Indexeur()
    indexeur.preparer_collection(recreer=tout_reconstruire)

    if not tout_reconstruire:
        documents = _filtrer_les_inchanges(indexeur, documents)
        if not documents:
            logger.info("=== INGESTION : rien a faire ===")
            return {"documents": 0, "chunks": 0, "ignores": "inchanges"}

    chunks = decouper(documents)
    total = indexeur.indexer(chunks)

    statistiques = {"documents": len(documents), "chunks": total}
    logger.info("=== INGESTION : terminee %s ===", statistiques)
    return statistiques


def _filtrer_les_inchanges(indexeur, documents: list) -> list:
    """Ne conserve que les documents absents ou modifies.

    Pour un document modifie, on SUPPRIME d'abord ses anciens
    chunks : sans cela, l'index contiendrait les deux versions,
    et le retriever remonterait joyeusement la perimee.
    """
    presentes = _empreintes_indexees(indexeur)
    a_traiter, deja_supprimes = [], set()

    for document in documents:
        empreinte = document.metadata.get("empreinte")
        source = document.metadata.get("source")

        if empreinte in presentes:
            continue                      # inchange : on passe

        # Nouveau ou modifie. Si une version de ce fichier existe
        # deja dans l'index, on l'efface avant de reindexer.
        if source not in deja_supprimes:
            indexeur.client.delete(
                collection_name=indexeur.collection,
                points_selector=Filter(must=[FieldCondition(
                    key="source", match=MatchValue(value=source),
                )]),
            )
            deja_supprimes.add(source)

        a_traiter.append(document)

    logger.info("Incremental : %d sections a retraiter sur %d",
                len(a_traiter), len(documents))
    return a_traiter


def _empreintes_indexees(indexeur) -> set[str]:
    """Parcourt l'index et collecte les empreintes deja presentes."""
    empreintes, curseur = set(), None
    while True:
        points, curseur = indexeur.client.scroll(
            collection_name=indexeur.collection,
            limit=1000, offset=curseur, with_payload=["empreinte"],
        )
        empreintes.update(p.payload.get("empreinte", "") for p in points)
        if curseur is None:
            return empreintes
