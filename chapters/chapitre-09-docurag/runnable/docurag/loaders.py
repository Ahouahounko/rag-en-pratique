"""Chargement local de documents textuels et PDF optionnels."""

from __future__ import annotations

import hashlib
from pathlib import Path

from rag_en_pratique.core import Document

KNOWN_DEPARTMENTS = {"rh", "finance", "juridique", "it", "produit", "commercial"}


def fingerprint(path: Path) -> str:
    """Calcule une empreinte du contenu, stable malgré les changements de date."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def department(path: Path) -> str:
    for part in path.parts:
        if part.lower() in KNOWN_DEPARTMENTS:
            return part
    return "general"


def metadata(path: Path) -> dict[str, object]:
    return {
        "source": path.name,
        "source_path": str(path),
        "extension": path.suffix.lower(),
        "department": department(path),
        "fingerprint": fingerprint(path),
    }


def load_text(path: Path) -> Document:
    return Document(text=path.read_text(encoding="utf-8"), metadata=metadata(path))


def load_pdf(path: Path) -> list[Document]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError('Installez le support PDF avec pip install -e ".[pdf]"') from exc
    reader = PdfReader(path)
    return [
        Document(
            text=page.extract_text() or "",
            metadata={**metadata(path), "page": page_number},
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
