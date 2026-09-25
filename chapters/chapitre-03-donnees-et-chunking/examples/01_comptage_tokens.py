"""Mesurer la taille en tokens et brancher ce compteur dans un splitter."""

import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

ENCODER = tiktoken.get_encoding("cl100k_base")


def compter_tokens(texte: str) -> int:
    """Retourne le nombre de tokens produits par l'encodage choisi."""

    return len(ENCODER.encode(texte))


def creer_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=640,
        chunk_overlap=64,
        length_function=compter_tokens,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def main() -> None:
    anglais = "The retrieval system returns relevant documents."
    francais = "Le système de récupération renvoie les documents pertinents."
    print("Anglais :", compter_tokens(anglais), "tokens")
    print("Français :", compter_tokens(francais), "tokens")
    print("Splitter prêt :", creer_splitter())


if __name__ == "__main__":
    main()
