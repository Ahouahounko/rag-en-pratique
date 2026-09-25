import runpy
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "chapters/chapitre-05-bases-vectorielles/examples"


def load(filename: str) -> dict[str, object]:
    return runpy.run_path(str(EXAMPLES / filename))


class FakeResponses:
    def __init__(self, *texts: str) -> None:
        self.texts = iter(texts)

    def create(self, **kwargs: object) -> SimpleNamespace:
        assert kwargs["model"] == "modele-test"
        return SimpleNamespace(output_text=next(self.texts))


class FakeClient:
    def __init__(self, *texts: str) -> None:
        self.responses = FakeResponses(*texts)


def test_faiss_hnsw_and_ivf_find_the_query_vector() -> None:
    hnsw = load("01_faiss_hnsw.py")
    vectors = np.array([[1, 0], [0, 1], [0.8, 0.2]], dtype=np.float32)
    index = hnsw["construire_index_hnsw"](vectors, 2, m=4)
    _, positions = hnsw["chercher"](index, vectors[0], k=1)
    assert positions.tolist() == [0]

    ivf = load("02_faiss_ivf.py")
    corpus = np.vstack([vectors, [[0.2, 0.8], [0.7, 0.3], [0.3, 0.7]]]).astype(np.float32)
    index = ivf["construire_index_ivf"](corpus, 2, n_list=2)
    _, positions = ivf["chercher"](index, corpus[0], k=1, nprobe=2)
    assert positions.tolist() == [0]


def test_self_query_and_multi_query_accept_injected_clients() -> None:
    self_query = load("07_self_query.py")
    structured = self_query["construire_self_query"](
        "Contrats juridiques",
        client=FakeClient('{"texte":"contrats","filtres":{"departement":"juridique"}}'),
        model="modele-test",
    )
    assert structured.texte == "contrats"
    assert structured.filtres == {"departement": "juridique"}

    multi = load("08_multi_query.py")
    variants = multi["generer_variantes"](
        "retour",
        2,
        client=FakeClient("délai de retour\npolitique de remboursement"),
        model="modele-test",
    )
    assert variants == ["retour", "délai de retour", "politique de remboursement"]
    assert multi["fusion_rrf"]([["a", "b"], ["b", "a"]]) == ["a", "b"]


def test_ensemble_and_text_to_sql_are_bounded() -> None:
    ensemble = load("09_ensemble.py")
    documents = ["retour trente jours", "garantie deux ans", "livraison cinq jours"]
    rechercher = ensemble["construire_ensemble"](
        documents,
        lambda question, k: documents[:k],
    )
    assert rechercher("retour", 2)[0] == "retour trente jours"

    text_to_sql = load("10_text_to_sql.py")
    assert text_to_sql["valider_select"]("SELECT * FROM ventes;", {"ventes"}) == (
        "SELECT * FROM ventes"
    )
    connection = sqlite3.connect(":memory:")
    connection.executescript("CREATE TABLE ventes(montant REAL); INSERT INTO ventes VALUES (2.5);")
    chain = text_to_sql["construire_text_to_sql"](
        connection,
        {"ventes"},
        client=FakeClient("SELECT SUM(montant) FROM ventes"),
        model="modele-test",
    )
    assert chain("total")["resultat"] == [(2.5,)]


def test_router_iterative_and_adaptive_rag() -> None:
    router = load("11_router_rag.py")
    assert router["router"](
        "combien ?", client=FakeClient("tables"), model="modele-test"
    ).value == "tables"

    iterative = load("13_rag_iteratif.py")

    class Retriever:
        def invoke(self, question: str) -> list[SimpleNamespace]:
            return [SimpleNamespace(page_content=f"Source pour {question}")]

    result = iterative["rag_iteratif"](
        "question",
        Retriever(),
        client=FakeClient("SUFFISANT", "Réponse [1]"),
        model="modele-test",
    )
    assert result["tours"] == 1
    assert result["reponse"] == "Réponse [1]"

    adaptive = load("14_rag_adaptatif.py")
    decision = adaptive["decider"](
        "politique interne", client=FakeClient("chercher"), model="modele-test"
    )
    assert decision.value == "chercher"


def test_production_retriever_reorders_with_injected_models() -> None:
    module = load("12_retriever_production.py")

    class Encoder:
        def encode(self, text: str, *, normalize_embeddings: bool) -> np.ndarray:
            assert text == "retour"
            assert normalize_embeddings
            return np.array([1.0, 0.0])

    class Reranker:
        def predict(self, pairs: list[tuple[str, str]]) -> list[float]:
            assert len(pairs) == 2
            return [0.1, 0.9]

    class Qdrant:
        def query_points(self, **kwargs: object) -> SimpleNamespace:
            assert kwargs["limit"] == 20
            return SimpleNamespace(
                points=[
                    SimpleNamespace(payload={"texte": "A", "source": "a"}, score=0.8),
                    SimpleNamespace(payload={"texte": "B", "source": "b"}, score=0.7),
                ]
            )

    retriever = module["RetrieverProduction"](Qdrant(), "docs", Encoder(), Reranker())
    results = retriever.chercher("retour")
    assert [result.source for result in results] == ["b", "a"]
