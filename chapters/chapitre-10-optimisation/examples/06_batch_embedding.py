"""Vectorisation par lots avec reprise exponentielle et progression."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable, Sequence

logger = logging.getLogger(__name__)


def _encoder(encodeur, textes: Sequence[str]) -> list[list[float]]:
    if hasattr(encodeur, "embed"):
        return encodeur.embed(textes)
    return encodeur.encode(list(textes))


def vectoriser_lot(
    textes: Sequence[str],
    encodeur,
    *,
    tentatives: int = 5,
    attente_initiale: float = 2.0,
    exceptions_reessayables: tuple[type[Exception], ...] = (TimeoutError, ConnectionError),
    dormir: Callable[[float], None] = time.sleep,
) -> list[list[float]]:
    for tentative in range(tentatives):
        try:
            return _encoder(encodeur, textes)
        except exceptions_reessayables:
            if tentative == tentatives - 1:
                raise
            dormir(attente_initiale * (2**tentative))
    raise RuntimeError("Boucle de reprise incohérente")


def vectoriser_corpus(
    chunks: Sequence[str],
    encodeur,
    *,
    taille_lot: int = 512,
    pause: float = 0.1,
    dormir: Callable[[float], None] = time.sleep,
) -> list[list[float]]:
    if taille_lot <= 0 or pause < 0:
        raise ValueError("taille_lot doit être positif et pause ne peut pas être négative")
    if not chunks:
        return []

    vectors: list[list[float]] = []
    batch_count = (len(chunks) + taille_lot - 1) // taille_lot
    started = time.perf_counter()
    for number in range(batch_count):
        batch = chunks[number * taille_lot : (number + 1) * taille_lot]
        vectors.extend(vectoriser_lot(batch, encodeur, dormir=dormir))
        if pause and number < batch_count - 1:
            dormir(pause)
        elapsed = time.perf_counter() - started
        remaining = elapsed / len(vectors) * (len(chunks) - len(vectors))
        logger.info(
            "%d/%d chunks (%.0f %%) — reste ~%.0f s",
            len(vectors),
            len(chunks),
            100 * len(vectors) / len(chunks),
            remaining,
        )
    return vectors


if __name__ == "__main__":
    class EncodeurDemo:
        def embed(self, textes: Sequence[str]) -> list[list[float]]:
            return [[float(len(texte)), 1.0] for texte in textes]

    print(vectoriser_corpus(["un", "deux", "trois"], EncodeurDemo(), taille_lot=2, pause=0))
