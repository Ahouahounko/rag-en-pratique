"""Découpage à taille fixe : la ligne de base à mesurer."""

import tiktoken

ENCODER = tiktoken.get_encoding("cl100k_base")


def decoupage_fixe(texte: str, taille: int = 512, overlap: int = 50) -> list[str]:
    if taille <= 0 or overlap < 0 or overlap >= taille:
        raise ValueError("Il faut taille > 0 et 0 <= overlap < taille")
    tokens = ENCODER.encode(texte)
    pas = taille - overlap
    chunks: list[str] = []
    for debut in range(0, len(tokens), pas):
        fenetre = tokens[debut : debut + taille]
        chunks.append(ENCODER.decode(fenetre))
        if debut + taille >= len(tokens):
            break
    return chunks


if __name__ == "__main__":
    texte = "Le RAG relie une question à des documents pertinents. " * 20
    for index, chunk in enumerate(decoupage_fixe(texte, taille=40, overlap=8), start=1):
        print(index, len(ENCODER.encode(chunk)), "tokens", repr(chunk[:55]))
