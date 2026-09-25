# src/ingestion/chunker.py
import logging

from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import get_settings

logger = logging.getLogger(__name__)

# Du plus structurant au moins structurant. Cet ordre EST la
# strategie : on ne coupe au milieu d'une phrase qu'en dernier
# recours, quand aucune frontiere plus haute ne suffit.
SEPARATEURS = ["\n\n", "\n", ". ", ", ", " ", ""]


def decouper(documents: list[Document]) -> list[Document]:
    """Decoupe les documents en preservant leurs metadonnees."""
    config = get_settings()

    decoupeur = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,        # PLAFOND, pas cible
        chunk_overlap=config.chunk_overlap,
        separators=SEPARATEURS,
        length_function=len,
    )

    chunks = decoupeur.split_documents(documents)

    # Chaque chunk garde une trace de sa position dans le corpus :
    # utile pour le debogage et pour un eventuel parent-child.
    for position, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = position
        chunk.metadata["chunk_size"] = len(chunk.page_content)

    if chunks:
        moyenne = sum(len(c.page_content) for c in chunks) / len(chunks)
        logger.info(
            "Decoupage : %d sections -> %d chunks "
            "(moyenne %.0f caracteres, plafond %d, recouvrement %d)",
            len(documents), len(chunks), moyenne,
            config.chunk_size, config.chunk_overlap,
        )

    return chunks
