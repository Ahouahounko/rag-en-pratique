"""Découpage récursif qui privilégie les frontières Markdown."""

import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

ENCODER = tiktoken.get_encoding("cl100k_base")


def compter_tokens(texte: str) -> int:
    return len(ENCODER.encode(texte))


def decoupage_recursif(document: str, taille: int = 120, overlap: int = 12) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=taille,
        chunk_overlap=overlap,
        length_function=compter_tokens,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(document)


if __name__ == "__main__":
    document = "# Guide\n\n## Retours\n\n" + "Retour accepté sous 30 jours. " * 15
    document += "\n## Livraison\n\n" + "Livraison en trois à cinq jours. " * 15
    for index, chunk in enumerate(decoupage_recursif(document), start=1):
        print(f"Chunk {index} ({compter_tokens(chunk)} tokens) :", repr(chunk[:70]))
