"""Chargement tolérant avec métadonnées et empreinte de contenu."""

from __future__ import annotations

import hashlib
from pathlib import Path

from rag_en_pratique.core import Document

KNOWN_DEPARTMENTS = {"rh", "finance", "juridique", "it", "produit", "commercial"}


def empreinte(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def departement(path: Path) -> str:
    return next((part for part in path.parts if part.lower() in KNOWN_DEPARTMENTS), "general")


def charger_dossier(directory: Path) -> list[Document]:
    if not directory.is_dir():
        raise FileNotFoundError(f"Dossier introuvable : {directory}")
    documents: list[Document] = []
    for path in sorted(directory.rglob("*")):
        if (
            path.is_file()
            and path.suffix.lower() in {".md", ".txt"}
            and path.name.lower() != "readme.md"
        ):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                print(f"Ignoré : {path.name} ({error})")
                continue
            documents.append(
                Document(
                    text,
                    {
                        "source": path.name,
                        "source_path": str(path),
                        "department": departement(path),
                        "fingerprint": empreinte(path),
                    },
                )
            )
    return documents


if __name__ == "__main__":
    print(f"{len(charger_dossier(Path('data/sample')))} document(s) chargé(s)")
