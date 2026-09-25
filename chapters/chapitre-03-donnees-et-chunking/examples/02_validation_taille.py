"""Valider les tailles avant d'appeler un modèle d'embedding."""

import logging

import tiktoken

MAX_TOKENS = 512
MARGE = 0.90
ENCODER = tiktoken.get_encoding("cl100k_base")
logger = logging.getLogger(__name__)


def compter_tokens(texte: str) -> int:
    return len(ENCODER.encode(texte))


def valider_chunks(chunks: list[str]) -> tuple[list[str], list[str]]:
    """Sépare les chunks conformes de ceux qui doivent être redécoupés."""

    conformes: list[str] = []
    a_redecouper: list[str] = []
    seuil = int(MAX_TOKENS * MARGE)
    for chunk in chunks:
        nombre = compter_tokens(chunk)
        if nombre > seuil:
            logger.warning("Chunk de %d tokens > seuil %d", nombre, seuil)
            a_redecouper.append(chunk)
        else:
            conformes.append(chunk)
    return conformes, a_redecouper


if __name__ == "__main__":
    petits, grands = valider_chunks(["Un chunk court.", "mot " * 600])
    print(f"Conformes : {len(petits)} — à redécouper : {len(grands)}")
