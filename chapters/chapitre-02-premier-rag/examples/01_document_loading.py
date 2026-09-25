"""Charge les documents de démonstration du chapitre 2."""

from __future__ import annotations

from pathlib import Path

from rag_en_pratique.core import Document


def load_markdown_documents(directory: Path) -> list[Document]:
    return [
        Document(path.read_text(encoding="utf-8"), {"source": path.name})
        for path in sorted(directory.glob("*.md"))
        if path.name.lower() != "readme.md"
    ]


def main() -> None:
    repository = Path(__file__).resolve().parents[3]
    documents = load_markdown_documents(repository / "data" / "sample")
    for document in documents:
        print(document.metadata["source"], len(document.text), "caractères")


if __name__ == "__main__":
    main()
