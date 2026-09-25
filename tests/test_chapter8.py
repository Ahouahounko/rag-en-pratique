import runpy
from pathlib import Path
from types import SimpleNamespace

from rag_en_pratique.observability import PassageEvaluation

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "chapters/chapitre-08-observabilite/examples"


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


def test_reference_set_contains_three_question_types() -> None:
    generator = load("01_generation_jeu.py")["generer_jeu"]
    passages = [
        PassageEvaluation("a", "Garantie 24 mois", "cgv.pdf"),
        PassageEvaluation("b", "Retour sous 30 jours", "cgv.pdf"),
    ]
    dataset = generator(
        passages,
        3,
        {"directe": 1 / 3, "synthese": 1 / 3, "sans_reponse": 1 / 3},
        ["garantie du produit Z"],
        client=FakeClient(
            "Quelle garantie ?",
            "24 mois",
            "Comparez garantie et retour.",
            "Garantie 24 mois, retour 30 jours.",
            "Quelle garantie pour Z ?",
        ),
        model="modele-test",
    )
    assert {item["type"] for item in dataset} == {"directe", "synthese", "sans_reponse"}


def test_discriminating_questions_and_filtering_accept_fake_clients() -> None:
    discriminating = load("02_questions_discriminantes.py")
    target = PassageEvaluation("a", "Garantie 24 mois", "cgv.pdf")
    neighbor = PassageEvaluation("b", "Garantie commerciale 12 mois", "cgv.pdf")

    class Index:
        def chercher(self, text: str, k: int) -> list[PassageEvaluation]:
            assert text == target.texte and k == 3
            return [target, neighbor]

    result = discriminating["generer_question_discriminante"](
        target,
        Index(),
        client=FakeClient('{"question":"Durée standard ?","reponse":"24 mois"}'),
        model="modele-test",
    )
    assert result["distracteurs_connus"] == ["b"]

    filtering = load("03_filtrage_questions.py")
    kept = filtering["filtrer"](
        [{"question": "Maison avec jardin ?"}, {"question": "Couleur de la troisième brique ?"}],
        client=FakeClient("Naturelle.\nNote : 5", "Artificielle.\nNote : 1"),
        model="modele-test",
    )
    assert [item["note_realisme"] for item in kept] == [5]


def test_judge_keeps_normalized_and_raw_results() -> None:
    judge = load("05_execution_juge.py")
    verdict = judge["juger"](
        "Durée ?",
        "Garantie 24 mois.",
        "24 mois.",
        client=FakeClient("JUSTIFICATION : Tout est étayé.\nNOTE : 5"),
        model="modele-test",
    )
    assert verdict.note == 1.0
    assert verdict.note_brute == 5
    assert verdict.justification == "Tout est étayé."


def test_campaign_and_non_regression_have_distinct_outputs() -> None:
    module = load("06_deux_outils.py")
    case = module["CasDeTest"]("Durée ?", "24 mois", "Garantie 24 mois")
    measure = lambda item: float(item.reponse in item.contexte)
    report = module["evaluer_campagne"]([case], {"fidelite": measure})
    assert report["moyennes"]["fidelite"] == 1.0
    assert module["verifier_non_regression"](case, measure, 0.8) == 1.0


def test_failure_matrix_identifies_all_four_categories() -> None:
    module = load("07_matrice_attribution.py")

    class System:
        def repondre(self, question: str) -> dict[str, object]:
            source_ok = question in {"nominal", "generateur"}
            answer_ok = question in {"nominal", "ancrage"}
            sources = [SimpleNamespace(id="attendu")] if source_ok else []
            return {"sources": sources, "reponse": "ok" if answer_ok else "faux"}

    dataset = [
        {"question": name, "passages_attendus": ["attendu"], "reponse": "ok"}
        for name in ("nominal", "generateur", "retriever", "ancrage")
    ]
    result = module["attribuer_defaillances"](
        dataset,
        System(),
        lambda question, answer, reference: answer == reference,
    )
    assert set(result["exemples"]) == {"nominal", "generateur", "retriever", "ancrage"}
    assert result["alerte_ancrage"] is True


def test_context_substitution_latency_and_drift_are_local() -> None:
    substitution = load("08_substitution_contexte.py")

    class System:
        def repondre(self, question: str) -> dict[str, str]:
            return {"reponse": "Réponse mémorisée"}

        def generer_avec(self, question: str, contexte: list[str]) -> str:
            assert contexte
            return "Les documents fournis ne permettent pas de répondre."

    anchoring = substitution["tester_ancrage"](
        [{"question": "Question"}], System(), ["corpus étranger"]
    )
    assert anchoring["taux_abstention"] == 1.0

    latency = load("09_percentiles.py")
    tracker = latency["SuiviLatence"](minimum=5)
    for value in [10, 11, 12, 13, 100]:
        tracker.enregistrer("total", value)
    assert tracker.percentiles()["total"]["p95"] == 100

    drift = load("10_detection_drift.py")
    alerts = drift["detecter_derive"](
        {"qualite": [0.9] * 30, "latence": [100.0] * 30},
        {"qualite": [0.7] * 30, "latence": [180.0] * 30},
        plus_grand_est_meilleur={"qualite": True, "latence": False},
    )
    assert {alert["sens"] for alert in alerts} == {"degradation"}
