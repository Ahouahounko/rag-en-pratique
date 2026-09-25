"""Late Chunking illustré avec un encodeur long-contexte pédagogique."""

import numpy as np
import tiktoken


class ModeleLongContextePedagogique:
    """Produit un vecteur par token enrichi par la moyenne du document."""

    def __init__(self, dimension: int = 8) -> None:
        self.dimension = dimension
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def encode_tokens(self, document: str) -> np.ndarray:
        ids = np.array(self.tokenizer.encode(document), dtype=float)
        dimensions = np.arange(1, self.dimension + 1, dtype=float)
        locaux = np.sin(ids[:, None] / dimensions[None, :])
        contexte_global = locaux.mean(axis=0, keepdims=True)
        return locaux + contexte_global


def late_chunking(
    document: str,
    modele_long_contexte: ModeleLongContextePedagogique,
    frontieres: list[tuple[int, int]],
) -> list[np.ndarray]:
    vecteurs_tokens = modele_long_contexte.encode_tokens(document)
    return [vecteurs_tokens[debut:fin].mean(axis=0) for debut, fin in frontieres]


def frontieres_en_tokens(
    document: str,
    chunk_size_chars: int,
    tokenizer: tiktoken.Encoding,
) -> list[tuple[int, int]]:
    frontieres: list[tuple[int, int]] = []
    for debut_caractere in range(0, len(document), chunk_size_chars):
        fin_caractere = min(debut_caractere + chunk_size_chars, len(document))
        debut_token = len(tokenizer.encode(document[:debut_caractere]))
        fin_token = len(tokenizer.encode(document[:fin_caractere]))
        if fin_token > debut_token:
            frontieres.append((debut_token, fin_token))
    return frontieres


if __name__ == "__main__":
    document = (
        "Les retours sont acceptés sous trente jours. "
        "La livraison standard prend cinq jours ouvrés."
    )
    modele = ModeleLongContextePedagogique()
    frontieres = frontieres_en_tokens(document, 45, modele.tokenizer)
    vecteurs = late_chunking(document, modele, frontieres)
    for frontiere, vecteur in zip(frontieres, vecteurs, strict=True):
        texte = modele.tokenizer.decode(modele.tokenizer.encode(document)[slice(*frontiere)])
        print(frontiere, repr(texte), "->", np.round(vecteur[:3], 3))
