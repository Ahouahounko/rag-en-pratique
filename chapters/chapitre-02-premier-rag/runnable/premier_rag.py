"""Premier pipeline RAG exécutable, sans service externe par défaut."""

from __future__ import annotations

from pathlib import Path

from rag_en_pratique.core import (
    Document,
    InMemoryVectorStore,
    RAGPipeline,
    split_documents,
)
from rag_en_pratique.openai_adapter import OpenAIEmbedder, OpenAIGenerator


def load_markdown_documents(directory: Path) -> list[Document]:
    return [
        Document(text=path.read_text(encoding="utf-8"), metadata={"source": path.name})
        for path in sorted(directory.glob("*.md"))
        if path.name.lower() != "readme.md"
    ]


def build_pipeline(data_directory: Path) -> RAGPipeline:
    documents = load_markdown_documents(data_directory)
    chunks = split_documents(documents, chunk_size=60, overlap=10)
    store = InMemoryVectorStore(OpenAIEmbedder())
    store.add(chunks)
    return RAGPipeline(store, OpenAIGenerator())


def main() -> None:
    repository = Path(__file__).resolve().parents[3]
    pipeline = build_pipeline(repository / "data" / "sample")
    result = pipeline.ask("Sous combien de jours peut-on retourner un produit ?")
    print(result["answer"])


if __name__ == "__main__":
    main()
