# src/api/main.py
import logging
import time
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from qdrant_client import QdrantClient

from src.api.schemas import (
    RequeteIngestion, RequeteQuestion, ReponseQuestion, Sante,
)
from src.config import get_settings
from src.generation.generator import Generateur
from src.ingestion import ingerer
from src.retrieval.retriever import RetrieverHybride

logger = logging.getLogger(__name__)
config = get_settings()

composants: dict = {}


@asynccontextmanager
async def cycle_de_vie(app: FastAPI):
    """Charge les modeles UNE FOIS au demarrage.

    Les instancier a chaque requete rechargerait plusieurs
    centaines de Mo par appel : le service serait inutilisable.
    """
    logger.info("Chargement des composants...")
    composants["retriever"] = RetrieverHybride()
    composants["generateur"] = Generateur()
    logger.info("Composants prets.")
    yield
    composants.clear()


app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    description="Assistant documentaire RAG",
    lifespan=cycle_de_vie,
)

# En production, remplacer par la liste des origines autorisees.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/health", response_model=Sante, tags=["Supervision"])
async def sante():
    """Verifie que l'API ET la base vectorielle repondent.

    Un healthcheck qui ne teste que l'API renvoie "en bonne
    sante" alors que Qdrant est tombe : inutile.
    """
    client = QdrantClient(url=config.qdrant_url)
    infos = client.get_collection(config.qdrant_collection)
    return Sante(
        statut="ok",
        version=config.app_version,
        collection={
            "nom": config.qdrant_collection,
            "points": infos.points_count,
        },
    )


@app.post("/query", response_model=ReponseQuestion, tags=["RAG"])
async def interroger(requete: RequeteQuestion):
    """Pipeline complet : recherche puis generation."""
    depart = time.perf_counter()
    filtres = ({"departement": requete.departement}
               if requete.departement else None)

    try:
        passages = composants["retriever"].chercher(
            requete.question, filtres=filtres)
        reponse = composants["generateur"].repondre(
            requete.question, passages)

        duree = int((time.perf_counter() - depart) * 1000)
        logger.info("query | %d ms | %d passages | confiance=%s | %r",
                    duree, reponse.nb_passages, reponse.confiance,
                    requete.question[:80])

        return ReponseQuestion(
            reponse=reponse.texte,
            sources=reponse.sources,
            confiance=reponse.confiance,
            nb_passages=reponse.nb_passages,
            version_prompt=reponse.version_prompt,
            duree_ms=duree,
        )

    except Exception as erreur:
        logger.error("Echec du pipeline : %s", erreur, exc_info=True)
        # On ne renvoie PAS le detail de l'exception au client :
        # il peut contenir des chemins ou des fragments de document.
        raise HTTPException(status_code=500,
                            detail="Erreur interne du service.")


@app.post("/query/stream", tags=["RAG"])
async def interroger_en_flux(requete: RequeteQuestion):
    """Meme pipeline, reponse diffusee au fil de l'eau (SSE)."""
    filtres = ({"departement": requete.departement}
               if requete.departement else None)
    passages = composants["retriever"].chercher(
        requete.question, filtres=filtres)

    async def flux():
        for jeton in composants["generateur"].diffuser(
                requete.question, passages):
            yield f"data: {jeton}\n\n"
        yield "data: [FIN]\n\n"

    return StreamingResponse(flux(), media_type="text/event-stream")


@app.post("/ingest", tags=["Administration"])
async def lancer_ingestion(requete: RequeteIngestion,
                           taches: BackgroundTasks):
    """Declenche l'ingestion EN TACHE DE FOND.

    Elle dure des minutes : la faire en synchrone provoquerait
    une expiration de la requete HTTP.
    """
    taches.add_task(
        ingerer,
        chemin=requete.chemin,
        urls=requete.urls,
        tout_reconstruire=requete.tout_reconstruire,
    )
    return {"message": "Ingestion lancee en arriere-plan",
            "tout_reconstruire": requete.tout_reconstruire}
