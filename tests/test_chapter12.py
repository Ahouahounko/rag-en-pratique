import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "chapters/chapitre-12-bonnes-pratiques/examples"


def load_example(filename: str) -> ModuleType:
    name = "chapter12_" + filename.removesuffix(".py")
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_cleaning_normalizes_without_rewriting_content() -> None:
    module = load_example("01_nettoyage.py")
    raw = "Titre\r\n\r\n 12 \r\nPhrase   importante.\x00\r\n"
    assert module.nettoyer_document(raw) == "Titre\n\nPhrase importante."


def test_chunking_harness_prefers_complete_answers_then_fewer_chunks() -> None:
    module = load_example("02_test_decoupage.py")

    def split(documents: list[str], *, taille: int, recouvrement: int) -> list[str]:
        del documents, recouvrement
        if taille == 10:
            return ["La réponse est", "trente jours"]
        return ["La réponse est trente jours"]

    class Index:
        def __init__(self, chunks: list[str]) -> None:
            self.chunks = chunks

        def chercher(self, question: str, *, k: int) -> list[str]:
            del question
            return self.chunks[:k]

    results = module.tester_decoupages(
        ["document"],
        [{"texte": "Quel délai ?", "reponse_attendue": "réponse est trente jours"}],
        [{"taille": 10, "recouvrement": 0}, {"taille": 20, "recouvrement": 0}],
        decouper=split,
        indexer=Index,
    )
    assert results[0]["taille"] == 20
    assert results[0]["complet"] == 1.0


def test_k_sweep_computes_recall_and_elbow() -> None:
    module = load_example("03_balayage_k.py")

    class Retriever:
        def chercher(self, question: str, *, k: int) -> list[SimpleNamespace]:
            del question
            return [SimpleNamespace(id=value) for value in ["a", "b", "c"][:k]]

    results = module.balayer_k(
        [{"texte": "question", "passages_attendus": {"a", "b"}}],
        Retriever(),
        [1, 2, 3],
    )
    assert results == [
        {"k": 1, "rappel": 0.5},
        {"k": 2, "rappel": 1.0},
        {"k": 3, "rappel": 1.0},
    ]
    assert module.choisir_coude(results, gain_minimal=0.01) == 2


def test_robust_prompt_contains_required_clauses_and_delimiters() -> None:
    prompt = (EXAMPLES / "04_prompt_robuste.txt").read_text(encoding="utf-8")
    for marker in ("ANCRAGE", "REFUS", "CITATION", "<extraits>", "</extraits>"):
        assert marker in prompt


def test_structured_logging_minimizes_content_by_default(caplog) -> None:
    module = load_example("05_journalisation.py")
    passage = SimpleNamespace(source="politique.md", page=1, score_rerank=0.8, score_dense=0.7)
    response = SimpleNamespace(
        texte="Réponse privée",
        confiance="Haut",
        version_prompt="1.2",
        tokens={"input": 10, "output": 3},
    )
    retriever = SimpleNamespace(chercher=lambda question: [passage])
    generator = SimpleNamespace(repondre=lambda question, passages: response)
    times = iter([0.0, 0.01, 0.03, 0.08])

    with caplog.at_level("INFO", logger="rag"):
        result = module.repondre_et_journaliser(
            "Question privée",
            "utilisateur@example.com",
            retriever,
            generator,
            secret="secret-test",
            horloge=lambda: next(times),
            trace_factory=lambda: "trace-test",
        )

    journal = result["journal"]
    assert journal["question"] == {"sha256": journal["question"]["sha256"], "longueur": 15}
    assert journal["latences_ms"]["total"] == 80
    serialized = json.dumps(journal, ensure_ascii=False)
    assert "Question privée" not in serialized
    assert "utilisateur@example.com" not in serialized


def test_static_audit_reports_critical_findings() -> None:
    module = load_example("06_audit.py")
    good = {
        "temperature": 0,
        "modele_embedding_ingestion": "model-a",
        "modele_embedding_requete": "model-a",
        "prompt_contient_clause_refus": True,
        "prompt_contient_clause_citation": True,
        "journalise_scores_retrieval": True,
        "journalise_question_reformulee": True,
        "filtrage_acces_au_retrieval": True,
        "golden_dataset_versionne": True,
        "k": 5,
    }
    assert module.auditer_configuration(good) == []
    findings = module.auditer_configuration({"temperature": 0.7, "k": 0})
    critical_codes = {finding.code for finding in findings if finding.critique}
    assert {"temperature", "embedding_manquant", "acl", "k_invalide"} <= critical_codes
