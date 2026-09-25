import json
import sys
from pathlib import Path

from rag_en_pratique.core import (
    Document,
    ExtractiveGenerator,
    HashingEmbedder,
    InMemoryVectorStore,
    RAGPipeline,
    split_document,
)

ROOT = Path(__file__).parents[1]


def test_offline_pipeline_finds_relevant_source() -> None:
    documents = [
        Document("Les retours sont acceptés pendant 30 jours.", {"source": "retours.md"}),
        Document("La livraison standard prend cinq jours.", {"source": "livraison.md"}),
    ]
    store = InMemoryVectorStore(HashingEmbedder())
    store.add(documents)
    result = RAGPipeline(store, ExtractiveGenerator()).ask(
        "Pendant combien de jours les retours sont-ils acceptés ?", top_k=1
    )
    assert result["sources"][0]["metadata"]["source"] == "retours.md"
    assert "30 jours" in result["answer"]
    assert "livraison standard" not in result["answer"]


def test_chunking_preserves_metadata() -> None:
    chunks = split_document(
        Document("un deux trois quatre cinq six", {"source": "test.md"}),
        chunk_size=4,
        overlap=1,
    )
    assert len(chunks) == 2
    assert chunks[1].metadata == {"source": "test.md", "chunk": 1, "start_word": 3}


def test_docurag_ingests_sample_documents() -> None:
    runnable = ROOT / "chapters" / "chapitre-09-docurag" / "runnable"
    sys.path.insert(0, str(runnable))
    try:
        from docurag import DocuRAG
        from docurag.config import Settings

        app = DocuRAG(Settings(use_openai=False, chunk_size=60, chunk_overlap=10))
        assert app.ingest(ROOT / "data" / "sample") >= 2
        result = app.ask("Quel est le délai pour retourner un produit ?")
        assert result["sources"]
        unknown = app.ask("Quel est le numéro de téléphone du directeur ?")
        assert "pas disponible" in unknown["answer"]
    finally:
        sys.path.remove(str(runnable))


def test_notebooks_are_clean_colab_notebooks() -> None:
    paths = [
        ROOT / "chapters/chapitre-02-premier-rag/02_premier_rag.ipynb",
        ROOT / "chapters/chapitre-09-docurag/09_docurag.ipynb",
    ]
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["nbformat"] == 4
        assert len(payload["cells"]) >= 10
        assert all(cell.get("outputs", []) == [] for cell in payload["cells"])
        assert all(cell.get("execution_count") is None for cell in payload["cells"])
        for cell in payload["cells"]:
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), str(path), "exec")
