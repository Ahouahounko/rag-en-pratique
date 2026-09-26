import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from rag_en_pratique.core import Document, InMemoryVectorStore

ROOT = Path(__file__).parents[1]
RUNNABLE = ROOT / "chapters/chapitre-09-docurag/runnable"
sys.path.insert(0, str(RUNNABLE))

from docurag.config import Settings
from docurag.generation import ABSTENTION, CitedGenerator
from docurag.loaders import fingerprint, load_directory
from docurag.pipeline import DocuRAG
from docurag.retrieval import HybridRetriever, Passage, reciprocal_rank_fusion


class KeywordEmbedder:
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [
            [float("retour" in text.lower()), float("livraison" in text.lower()), 0.1]
            for text in texts
        ]


class FakeGenerator:
    def generate(self, question: str, passages: list[object]) -> str:
        del question, passages
        return "Les retours sont acceptés sous 30 jours [Source 1]."


class FakeEmbeddingsAPI:
    def create(self, *, model: str, input: list[str]) -> SimpleNamespace:
        del model
        return SimpleNamespace(
            data=[SimpleNamespace(embedding=vector) for vector in KeywordEmbedder().embed(input)]
        )


class FakeResponsesAPI:
    def create(self, **kwargs: object) -> SimpleNamespace:
        del kwargs
        return SimpleNamespace(output_text="Réponse simulée [Source 1].")


class FakeOpenAIClient:
    def __init__(self) -> None:
        self.embeddings = FakeEmbeddingsAPI()
        self.responses = FakeResponsesAPI()


def test_settings_reject_invalid_chunk_overlap() -> None:
    with pytest.raises(ValueError, match="chunk_overlap"):
        Settings(chunk_size=10, chunk_overlap=10)


def test_loader_adds_fingerprint_and_department(tmp_path: Path) -> None:
    directory = tmp_path / "RH"
    directory.mkdir()
    path = directory / "politique.md"
    path.write_text("Télétravail deux jours par semaine.", encoding="utf-8")

    documents = load_directory(tmp_path)

    assert documents[0].metadata["department"] == "RH"
    assert documents[0].metadata["fingerprint"] == fingerprint(path)


def test_hybrid_retrieval_and_rrf() -> None:
    store = InMemoryVectorStore(KeywordEmbedder())
    store.add(
        [
            Document("Les retours sont acceptés sous 30 jours.", {"source": "retours.md"}),
            Document("La livraison prend cinq jours.", {"source": "livraison.md"}),
        ]
    )
    dense = store.search("Quel délai de retour ?", top_k=2)
    assert reciprocal_rank_fusion([dense, list(reversed(dense))])

    results = HybridRetriever(store, final_k=1).search("Quel délai de retour ?")
    assert results[0].source == "retours.md"


def test_cited_generator_abstains_and_preserves_source_order() -> None:
    generator = CitedGenerator(FakeGenerator())
    assert generator.answer("Question absente", []).answer == ABSTENTION

    passages = [
        Passage("Retour sous 30 jours.", "retours.md", dense_score=0.9),
        Passage("Livraison sous cinq jours.", "livraison.md", dense_score=0.6),
    ]
    response = generator.answer("Quel délai ?", passages)
    assert [source["document"] for source in response.sources] == [
        "retours.md",
        "livraison.md",
    ]
    assert response.confidence == "Haut"

    same_page = generator.answer(
        "Deux passages ?",
        [
            Passage("Premier fragment.", "manuel.pdf", page=2, dense_score=0.8),
            Passage("Second fragment.", "manuel.pdf", page=2, dense_score=0.7),
        ],
    )
    assert len(same_page.sources) == 2


def test_docurag_incremental_ingestion() -> None:
    app = DocuRAG(
        Settings(openai_model="modele-test", chunk_size=60, chunk_overlap=10),
        client=FakeOpenAIClient(),
    )
    assert app.ingest(ROOT / "data/sample", rebuild=True) >= 2
    assert app.ingest(ROOT / "data/sample") == 0
    response = app.ask("Quel est le délai de retour ?")
    assert response["sources"][0]["document"] == "politique_retours.md"
    assert response["prompt_version"] == "1.2"
