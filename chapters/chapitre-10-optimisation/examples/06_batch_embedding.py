import logging
import time

from tenacity import (
    retry, retry_if_exception_type,
    stop_after_attempt, wait_exponential,
)

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(5),
    # Attente exponentielle : 2 s, 4 s, 8 s, 16 s. C'est ce que
    # les fournisseurs attendent quand ils renvoient un depassement
    # de quota ; reessayer immediatement aggrave la situation.
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=retry_if_exception_type(Exception),
)
def _vectoriser_lot(textes: list[str], encodeur) -> list[list[float]]:
    return encodeur.encode(textes)


def vectoriser_corpus(chunks: list[str], encodeur,
                      taille_lot: int = 512,
                      pause: float = 0.1) -> list[list[float]]:
    """Vectorise un grand corpus par lots.

    taille_lot : 512 est un bon compromis. Plus grand accelere
                 marginalement et augmente le cout d'un echec,
                 puisque tout le lot est a refaire.
    pause      : petite temporisation entre les lots, pour ne pas
                 saturer le quota. A augmenter si vous voyez des
                 depassements dans les journaux.
    """
    vecteurs = []
    nb_lots = (len(chunks) + taille_lot - 1) // taille_lot
    depart = time.perf_counter()

    for numero in range(nb_lots):
        lot = chunks[numero * taille_lot:(numero + 1) * taille_lot]
        vecteurs.extend(_vectoriser_lot(lot, encodeur))

        if pause and numero < nb_lots - 1:
            time.sleep(pause)

        if (numero + 1) % 10 == 0 or numero == nb_lots - 1:
            traites = len(vecteurs)
            ecoule = time.perf_counter() - depart
            restant = ecoule / traites * (len(chunks) - traites)
            logger.info("%d/%d chunks (%.0f %%) - reste ~%.0f s",
                        traites, len(chunks),
                        100 * traites / len(chunks), restant)

    return vecteurs
