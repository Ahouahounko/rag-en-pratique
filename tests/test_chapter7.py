import math
import runpy
from pathlib import Path
from types import SimpleNamespace

from rag_en_pratique.prompting import Passage

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "chapters/chapitre-07-evaluation/examples"


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


def test_rank_metrics_cover_presence_order_and_recall() -> None:
    metrics = load("01_metriques_rang.py")["evaluer_classement"](
        ["hors_sujet", "utile_1", "utile_2"],
        {"utile_1", "utile_2", "utile_3"},
        k=3,
    )
    assert metrics["hit_rate"] == 1.0
    assert metrics["precision_at_k"] == 2 / 3
    assert metrics["recall_at_k"] == 2 / 3
    assert metrics["mrr"] == 0.5
    assert 0 < metrics["ndcg"] < 1


def test_graded_ndcg_is_one_for_the_ideal_order() -> None:
    ndcg = load("02_ndcg_gradue.py")["ndcg_gradue"]
    relevance = {"a": 3, "b": 2, "c": 1}
    assert math.isclose(ndcg(["a", "b", "c"], relevance, k=3), 1.0)
    assert ndcg(["c", "b", "a"], relevance, k=3) < 1.0


def test_faithfulness_keeps_auditable_details() -> None:
    faithfulness = load("03_fidelite_maison.py")["calculer_faithfulness"]
    result = faithfulness(
        "La garantie dure 24 mois et elle est transférable.",
        "La garantie dure 24 mois.",
        client=FakeClient(
            "La garantie dure 24 mois.\nLa garantie est transférable.",
            "ETAYEE",
            "ABSENTE",
        ),
        model="modele-test",
    )
    assert result["score"] == 0.5
    assert result["total"] == 2
    assert result["detail"][1]["verdict"] == "ABSENTE"


def test_campaign_preserves_case_details_and_metadata() -> None:
    campaign = load("04_campagne_evaluation.py")

    class System:
        def repondre(self, question: str) -> dict[str, object]:
            assert question == "Quel délai ?"
            return {
                "reponse": "Le retour est possible sous 30 jours [doc_1].",
                "sources": [
                    Passage(
                        "Retour sous 30 jours.",
                        {"id": "retours_1", "source": "retours.md"},
                    )
                ],
            }

    report = campaign["lancer_campagne"](
        [
            {
                "question": "Quel délai ?",
                "passages_attendus": ["retours_1"],
                "type": "nominal",
                "sujet": "retours",
            }
        ],
        System(),
        {"version_jeu": "1.0", "modele_juge": "simule"},
        faithfulness=lambda answer, context: 1.0,
        answer_relevance=lambda question, answer: 0.9,
        contextual_precision=lambda question, sources: 1.0,
    )
    assert report["moyennes"]["contextual_recall"] == 1.0
    assert report["diagnostic"] == "Système sain. Surveiller sans intervenir."
    assert report["par_cas"][0]["sujet"] == "retours"
    assert report["metadonnees"]["version_jeu"] == "1.0"


def test_judge_score_is_clamped_and_diagnostics_are_actionable() -> None:
    campaign = load("04_campagne_evaluation.py")
    score = campaign["score_juge"](
        "pertinence",
        "question",
        "réponse",
        client=FakeClient("1.2"),
        model="modele-test",
    )
    assert score == 1.0
    assert "Retriever incomplet" in campaign["diagnostiquer"](
        {
            "faithfulness": 0.9,
            "answer_relevance": 0.9,
            "contextual_precision": 0.8,
            "contextual_recall": 0.5,
        }
    )
