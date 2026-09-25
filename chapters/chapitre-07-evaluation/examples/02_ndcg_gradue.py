"""Calculer le nDCG avec des annotations de pertinence graduées."""

from __future__ import annotations

import math


def gain(note: int, exponentiel: bool = True) -> float:
    if note < 0:
        raise ValueError("Une note de pertinence ne peut pas être négative")
    return float(2**note - 1 if exponentiel else note)


def ndcg_gradue(
    recuperes: list[str],
    pertinence: dict[str, int],
    k: int = 5,
    *,
    gain_exponentiel: bool = True,
) -> float:
    if k <= 0:
        raise ValueError("k doit être strictement positif")
    dcg = sum(
        gain(pertinence.get(document, 0), gain_exponentiel) / math.log2(rang + 1)
        for rang, document in enumerate(recuperes[:k], start=1)
    )
    meilleures = sorted(pertinence.values(), reverse=True)[:k]
    idcg = sum(
        gain(note, gain_exponentiel) / math.log2(rang + 1)
        for rang, note in enumerate(meilleures, start=1)
    )
    return dcg / idcg if idcg else 0.0


if __name__ == "__main__":
    notes = {"chunk_1": 3, "chunk_2": 2, "chunk_3": 1, "chunk_4": 0}
    print(round(ndcg_gradue(["chunk_3", "chunk_1", "chunk_4"], notes, k=3), 3))
