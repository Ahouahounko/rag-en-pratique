import math


def ndcg_gradue(recuperes: list[str],
                pertinence: dict[str, int],
                k: int = 5) -> float:
    """nDCG avec des notes de pertinence 0 a 3.

    pertinence : {"chunk_12": 3, "chunk_47": 1, ...}
                 0 = hors sujet, 1 = marginal,
                 2 = pertinent,  3 = hautement pertinent

    Les passages absents du dictionnaire sont supposes non
    pertinents : c'est la convention la plus sure, mais elle
    suppose une annotation exhaustive du jeu de reference.
    """
    tetes = recuperes[:k]

    # Gain reel : la note du passage, escomptee par sa position
    dcg = sum(pertinence.get(doc, 0) / math.log2(rang + 1)
              for rang, doc in enumerate(tetes, start=1))

    # Gain ideal : les MEMES notes, dans le meilleur ordre possible.
    # On trie toutes les notes connues, pas seulement les recuperees :
    # sinon on se compare a sa propre selection, ce qui masque les
    # passages qu'on a rates (cf. le piege du nDCG).
    meilleures = sorted(pertinence.values(), reverse=True)[:k]
    idcg = sum(note / math.log2(rang + 1)
               for rang, note in enumerate(meilleures, start=1))

    return dcg / idcg if idcg else 0.0
