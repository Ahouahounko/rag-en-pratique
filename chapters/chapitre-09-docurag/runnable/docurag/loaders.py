"""Chargement local de documents textuels et PDF optionnels."""

from __future__ import annotations

from pathlib import Path

from rag_en_pratique.core import Document


def load_text(path: Path) -> Document:
    return Document(text=path.read_text(encoding="utf-8"), metadata={"source": path.name})


def load_pdf(path: Path) -> list[Document]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError('Installez le support PDF avec pip install -e ".[pdf]"') from exc
    reader = PdfReader(path)
    return [
        Document(
            text=page.extract_text() or "",
            metadata={"source": path.name, "page": page_number},
        )
        for page_number, page in enumerate(reader.pages, start=1)
    ]


def load_directory(directory: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.name.lower() == "readme.md":
            continue
        if path.suffix.lower() in {".md", ".txt"}:
            documents.append(load_text(path))
        elif path.suffix.lower() == ".pdf":
            documents.extend(load_pdf(path))
    return [document for document in documents if document.text.strip()]
