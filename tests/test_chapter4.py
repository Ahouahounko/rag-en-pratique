import runpy
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "chapters/chapitre-04-retrieval-avance/examples"


def load(filename: str) -> dict[str, object]:
    return runpy.run_path(str(EXAMPLES / filename))


class FakeResponses:
    def __init__(self, text: str) -> None:
        self.text = text

    def create(self, **kwargs: object) -> SimpleNamespace:
        assert kwargs["model"] == "modele-test"
        return SimpleNamespace(output_text=self.text)


class FakeClient:
    def __init__(self, text: str) -> None:
        self.responses = FakeResponses(text)


def test_openai_helpers_accept_an_injected_client() -> None:
    rewriting = load("01_query_rewriting.py")
    rewritten = rewriting["reecrire_requete"](
        "Et le délai ?",
        ["Nous parlons de livraison."],
        client=FakeClient("Quel est le délai de livraison ?"),
        model="modele-test",
    )
    assert rewritten == "Quel est le délai de livraison ?"

    expansion = load("02_query_expansion.py")
    variants = expansion["generer_variantes"](
        "Délai de retour ?",
        2,
        client=FakeClient("Durée de rétractation\nÉchéance pour retourner un produit"),
        model="modele-test",
    )
    assert len(variants) == 3

    hyde = load("03_hyde.py")
    hypothesis = hyde["rediger_hypothese"](
        "Quel délai ?",
        client=FakeClient("Le retour est accepté sous trente jours."),
        model="modele-test",
    )
    assert "trente jours" in hypothesis


def test_rrf_and_hybrid_search_are_executable() -> None:
    expansion = load("02_query_expansion.py")
    passage = expansion["Passage"]
    first = passage("A", "a.md")
    second = passage("B", "b.md")
    fused = expansion["fusion_rrf"]([[first, second], [second, first]])
    assert set(fused) == {first, second}

    hybrid = load("04_hybrid_search.py")
    hybrid_passage = hybrid["Passage"]
    engine = hybrid["RechercheHybride"](
        [
            hybrid_passage("Garantie du SKU-4892 pendant deux ans.", "catalogue.md"),
            hybrid_passage("Livraison standard en cinq jours.", "livraison.md"),
        ]
    )
    assert engine.rechercher("SKU-4892", 1)[0].source == "catalogue.md"


def test_reranking_uses_pair_scores() -> None:
    reranking = load("05_reranking.py")
    passage = reranking["Passage"]

    class Retriever:
        def invoke(self, question: str) -> list[object]:
            del question
            return [passage("livraison", "a"), passage("retour", "b")]

    class Reranker:
        def predict(self, pairs: list[tuple[str, str]]) -> list[float]:
            assert len(pairs) == 2
            return [0.1, 0.9]

    result = reranking["rechercher_et_reclasser"](
        "retour",
        Retriever(),
        reranker=Reranker(),
        n_final=1,
    )
    assert result[0].source == "b"


def test_mmr_reorder_compression_and_pipeline() -> None:
    mmr = load("06_mmr_pseudocode.py")
    candidate = mmr["Candidat"]
    selected = mmr["selection_mmr"](
        [
            candidate("retour trente jours", "a"),
            candidate("retour délai trente jours", "b"),
            candidate("remboursement cinq jours", "c"),
        ],
        "retour et remboursement",
        2,
    )
    assert len(selected) == 2

    reorder = load("08_reorder.py")
    assert reorder["reordonner_pour_le_prompt"]([1, 2, 3, 4, 5, 6]) == [1, 3, 5, 6, 4, 2]

    compression = load("09_compression.py")
    compressed = compression["compresser_passage"](
        "Quel délai ?",
        compression["Passage"]("Le retour est possible sous trente jours.", "a.md"),
        client=FakeClient("Retour possible sous trente jours."),
        model="modele-test",
    )
    assert compressed.page_content == "Retour possible sous trente jours."

    pipeline = load("10_pipeline_ordre.py")
    pipeline_passage = pipeline["Passage"]
    corpus = [pipeline_passage("retour", "a", 0.9), pipeline_passage("hors sujet", "b", 0.1)]
    result = pipeline["pipeline_retrieval"]("retour", [lambda _: corpus], seuil=0.2)
    assert [item.source for item in result] == ["a"]
