"""Nettoyage conservateur d'un document avant le chunking."""

from __future__ import annotations

import re
import unicodedata

PAGE_NUMBER = re.compile(r"(?m)^\s*\d+\s*$")
CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def nettoyer_document(texte: str) -> str:
    """Normalise le bruit technique sans réécrire le contenu métier."""

    texte = unicodedata.normalize("NFC", texte)
    texte = texte.replace("\r\n", "\n").replace("\r", "\n")
    texte = CONTROL_CHARACTERS.sub("", texte)
    texte = PAGE_NUMBER.sub("", texte)
    texte = re.sub(r"[ \t]+", " ", texte)
    lignes = [ligne.strip() for ligne in texte.split("\n")]
    texte = "\n".join(lignes)
    texte = re.sub(r"\n{3,}", "\n\n", texte)
    return texte.strip()


if __name__ == "__main__":
    brut = "Titre\r\n\r\n  12  \r\nTexte   utile.\x00\r\n"
    print(nettoyer_document(brut))
