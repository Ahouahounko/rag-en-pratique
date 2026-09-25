import json
import sys
from pathlib import Path
from types import SimpleNamespace

from rag_en_pratique.core import (
    Document,
    InMemoryVectorStore,
    RAGPipeline,
    SearchResult,
    split_document,
)
from rag_en_pratique.openai_adapter import OpenAIEmbedder, OpenAIGenerator
from rag_en_pratique.providers import HuggingFaceEmbedder, HuggingFaceGenerator

ROOT = Path(__file__).parents[1]


class FakeEmbeddingsAPI:
    def create(self, *, model: str, input: list[str]) -> SimpleNamespace:
        del model
        data = []
        for text in input:
            lowered = text.lower()
            vector = [
                float("retour" in lowered),
                float("livraison" in lowered),
                0.1,
            ]
            data.append(SimpleNamespace(embedding=vector))
        return SimpleNamespace(data=data)


class FakeResponsesAPI:
    def create(self, **kwargs: object) -> SimpleNamespace:
        assert kwargs["model"] == "modele-test"
        return SimpleNamespace(output_text="Réponse OpenAI simulée avec citation [1].")


class FakeOpenAIClient:
    def __init__(self) -> None:
        self.embeddings = FakeEmbeddingsAPI()
        self.responses = FakeResponsesAPI()


class FakeEncoder:
    def encode(self, texts: list[str], *, normalize_embeddings: bool) -> list[list[float]]:
        assert normalize_embeddings is True
        return [[float(len(text)), 1.0] for text in texts]


class FakeTextPipeline:
    def __call__(self, messages: list[dict[str, str]], **kwargs: object) -> list[dict[str, object]]:
        assert messages[0]["role"] == "user"
        assert kwargs["do_sample"] is False
        return [{"generated_text": [*messages, {"role": "assistant", "content": "HF simulé [1]."}]}]


def test_openai_pipeline_with_injected_client() -> None:
    documents = [
        Document("Les retours sont acceptés pendant 30 jours.", {"source": "retours.md"}),
        Document("La livraison standard prend cinq jours.", {"source": "livraison.md"}),
    ]
    client = FakeOpenAIClient()
    store = InMemoryVectorStore(OpenAIEmbedder(client=client))
    store.add(documents)
    result = RAGPipeline(store, OpenAIGenerator("modele-test", client=client)).ask(
        "Pendant combien de jours les retours sont-ils acceptés ?", top_k=1
    )
    assert result["sources"][0]["metadata"]["source"] == "retours.md"
    assert result["answer"] == "Réponse OpenAI simulée avec citation [1]."


def test_generator_builds_grounded_openai_request() -> None:
    client = FakeOpenAIClient()
    generator = OpenAIGenerator("modele-test", client=client)
    passage = SearchResult(Document("Le retour dure 30 jours.", {"source": "retours.md"}), 1.0)
    assert "citation [1]" in generator.generate("Quel délai ?", [passage])


def test_huggingface_adapters_accept_injected_models() -> None:
    embedder = HuggingFaceEmbedder(encoder=FakeEncoder())
    assert embedder.embed(["bonjour"]) == [[7.0, 1.0]]
    generator = HuggingFaceGenerator(text_pipeline=FakeTextPipeline())
    passage = SearchResult(Document("Retour sous 30 jours.", {"source": "retours.md"}), 1.0)
    assert generator.generate("Quel délai ?", [passage]) == "HF simulé [1]."


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

        app = DocuRAG(
            Settings(openai_model="modele-test", chunk_size=60, chunk_overlap=10),
            client=FakeOpenAIClient(),
        )
        assert app.ingest(ROOT / "data" / "sample") >= 2
        result = app.ask("Quel est le délai pour retourner un produit ?")
        assert result["sources"]
    finally:
        sys.path.remove(str(runnable))


def test_notebooks_are_clean_colab_notebooks() -> None:
    paths = [
        ROOT / "chapters/chapitre-02-premier-rag/02_premier_rag.ipynb",
        ROOT / "chapters/chapitre-03-donnees-et-chunking/03_donnees_et_chunking.ipynb",
        ROOT / "chapters/chapitre-04-retrieval-avance/04_retrieval_avance.ipynb",
        ROOT / "chapters/chapitre-05-bases-vectorielles/05_bases_vectorielles.ipynb",
        ROOT / "chapters/chapitre-06-prompt-engineering/06_prompt_engineering.ipynb",
        ROOT / "chapters/chapitre-07-evaluation/07_evaluation.ipynb",
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
