# src/ingestion/loader.py
import hashlib
import logging
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader, Docx2txtLoader, TextLoader,
    UnstructuredExcelLoader, WebBaseLoader,
)
from langchain.schema import Document

logger = logging.getLogger(__name__)

# Extension -> loader. Ajouter un format = ajouter une ligne.
LOADERS = {
    ".pdf":  PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt":  TextLoader,
    ".md":   TextLoader,
    ".xlsx": UnstructuredExcelLoader,
}

DEPARTEMENTS = {"RH", "finance", "juridique", "IT",
                "produit", "commercial", "direction"}


def charger_dossier(chemin: str) -> list[Document]:
    """Charge recursivement un dossier, en enrichissant chaque
    document de ses metadonnees.

    Un fichier illisible est journalise et ignore : le lot
    continue. C'est un choix delibere (cf. texte).
    """
    racine = Path(chemin)
    if not racine.exists():
        raise FileNotFoundError(f"Dossier introuvable : {chemin}")

    documents, ignores = [], 0

    for fichier in racine.rglob("*"):
        if not fichier.is_file():
            continue

        extension = fichier.suffix.lower()
        if extension not in LOADERS:
            continue

        try:
            sections = LOADERS[extension](str(fichier)).load()
        except Exception as erreur:
            ignores += 1
            logger.error("Illisible, ignore : %s (%s)",
                         fichier.name, erreur)
            continue

        empreinte = _empreinte(fichier)

        for section in sections:
            section.metadata.update({
                "source": fichier.name,
                "source_path": str(fichier),
                "extension": extension,
                "departement": _departement(fichier),
                # L'empreinte permettra de detecter, a la prochaine
                # ingestion, si ce fichier a change (cf. section
                # sur la mise a jour incrementale).
                "empreinte": empreinte,
            })

        documents.extend(sections)
        logger.info("Charge : %s (%d sections)",
                    fichier.name, len(sections))

    logger.info("Chargement termine : %d sections, %d fichiers ignores",
                len(documents), ignores)
    return documents


def charger_urls(urls: list[str]) -> list[Document]:
    """Charge des pages web. Meme enrichissement, source = URL."""
    documents = WebBaseLoader(urls).load()
    for doc in documents:
        doc.metadata.setdefault("departement", "web")
    return documents


def _empreinte(fichier: Path) -> str:
    """Empreinte SHA-256 du CONTENU du fichier.

    On n'utilise pas la date de modification : une simple copie
    la change sans que le contenu bouge, ce qui declencherait
    des reindexations inutiles.
    """
    condensat = hashlib.sha256()
    with fichier.open("rb") as flux:
        for bloc in iter(lambda: flux.read(65536), b""):
            condensat.update(bloc)
    return condensat.hexdigest()


def _departement(fichier: Path) -> str:
    """Deduit le departement du chemin : documents/RH/... -> RH."""
    connus = {d.upper(): d for d in DEPARTEMENTS}
    for partie in fichier.parts:
        if partie.upper() in connus:
            return connus[partie.upper()]
    return "general"
