from rank_bm25 import BM25Okapi
import re


def preparer_bm25(chunks: list) -> BM25Okapi:
    """Construit l'index lexical a partir des memes chunks.

    La tokenisation doit etre IDENTIQUE a l'indexation et a la
    recherche, sinon "SKU-4892" et "sku 4892" ne se rencontreront
    jamais. C'est la premiere source de bug de cette technique.
    """
    corpus = [tokeniser(c.page_content) for c in chunks]
    return BM25Okapi(corpus)


def tokeniser(texte: str) -> list[str]:
    """Minuscules + decoupe sur tout ce qui n'est ni lettre ni chiffre.

    Le tiret de "SKU-4892" est conserve volontairement : c'est
    souvent ce qui rend la reference unique dans le corpus.
    """
    return re.findall(r"[a-z0-9\-]+", texte.lower())


def recherche_hybride(question: str, base_vectorielle, bm25,
                      chunks: list, k: int = 5) -> list:
    """Interroge les deux moteurs, puis fusionne par les rangs."""

    # On ratisse large des deux cotes : la fusion a besoin de
    # candidats pour reperer les documents trouves par les DEUX.
    n_candidats = k * 4

    # --- Voie 1 : semantique ---
    dense = base_vectorielle.similarity_search(question, k=n_candidats)

    # --- Voie 2 : lexicale ---
    scores = bm25.get_scores(tokeniser(question))
    meilleurs = sorted(range(len(scores)),
                       key=lambda i: scores[i], reverse=True)
    lexical = [chunks[i] for i in meilleurs[:n_candidats]]

    # --- Fusion : on reutilise la RRF du listing precedent ---
    return fusion_rrf([dense, lexical])[:k]
