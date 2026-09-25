"""Chargement des documents textuels de DocuRAG."""

from __future__ import annotations

from pathlib import Path

from rag_en_pratique.core import Document


def charger_dossier(directory: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(directory.rglob("*")):
        if (
            path.is_file()
            and path.suffix.lower() in {".md", ".txt"}
            and path.name.lower() != "readme.md"
        ):
            documents.append(
                Document(path.read_text(encoding="utf-8"), {"source": path.name})
            )
    return documents


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[3]
    print(f"{len(charger_dossier(repository / 'data' / 'sample'))} document(s) chargé(s)")
