"""Pipeline RAG complet du chapitre 2 avec fournisseur interchangeable."""

from __future__ import annotations

from pathlib import Path

from rag_en_pratique.core import (
    Document,
    InMemoryVectorStore,
    RAGPipeline,
    split_documents,
)
from rag_en_pratique.providers import create_provider


def load_documents(directory: Path) -> list[Document]:
    return [
        Document(path.read_text(encoding="utf-8"), {"source": path.name})
        for path in sorted(directory.glob("*.md"))
        if path.name.lower() != "readme.md"
    ]


def build_rag(documents_path: Path) -> RAGPipeline:
    chunks = split_documents(load_documents(documents_path), chunk_size=60, overlap=10)
    provider = create_provider()
    store = InMemoryVectorStore(provider.embedder)
    store.add(chunks)
    return RAGPipeline(store, provider.generator)


def main() -> None:
    repository = Path(__file__).resolve().parents[3]
    rag = build_rag(repository / "data" / "sample")
    result = rag.ask("Sous combien de jours peut-on retourner un produit ?")
    print(result["answer"])


if __name__ == "__main__":
    main()
