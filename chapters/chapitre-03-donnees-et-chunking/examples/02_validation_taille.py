import logging

MAX_TOKENS = 512          # plafond dur du modele (ex. BGE-large)
MARGE      = 0.90         # on ne remplit jamais a ras bord

logger = logging.getLogger(__name__)

def valider_chunks(chunks: list[str]) -> tuple[list[str], list[str]]:
    """
    Separe les chunks conformes de ceux qui seraient tronques.
    A brancher AVANT l'appel au modele d'embedding : c'est le seul
    endroit ou l'on peut encore detecter la troncature silencieuse.
    """
    conformes, a_redecouper = [], []
    seuil = int(MAX_TOKENS * MARGE)

    for chunk in chunks:
        n = compter_tokens(chunk)
        if n > seuil:
            logger.warning("Chunk de %d tokens > seuil %d : re-decoupage", n, seuil)
            a_redecouper.append(chunk)
        else:
            conformes.append(chunk)

    return conformes, a_redecouper
