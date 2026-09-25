# src/api/schemas.py
from pydantic import BaseModel, Field


class RequeteQuestion(BaseModel):
    """Entree de l'endpoint /query."""
    question: str = Field(
        ..., min_length=3, max_length=2000,
        description="Question en langue naturelle",
        examples=["Quelle est la politique de teletravail ?"],
    )
    departement: str | None = Field(
        None,
        description="Restreindre la recherche a un departement",
        examples=["RH"],
    )


class Source(BaseModel):
    document: str
    page: int
    departement: str
    pertinence: float


class ReponseQuestion(BaseModel):
    """Sortie de l'endpoint /query.

    On expose la confiance, le nombre de passages ET la version
    du prompt : sans cette derniere, impossible de savoir quelle
    version a produit une reponse signalee trois jours plus tard.
    """
    reponse: str
    sources: list[Source]
    confiance: str
    nb_passages: int
    version_prompt: str
    duree_ms: int


class RequeteIngestion(BaseModel):
    tout_reconstruire: bool = Field(
        False,
        description="Recreer l'index de zero au lieu d'un "
                    "traitement incremental",
    )
    chemin: str | None = None
    urls: list[str] | None = None


class Sante(BaseModel):
    statut: str
    version: str
    collection: dict
