import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "chapters/chapitre-10-optimisation/examples"


def load_example(filename: str) -> ModuleType:
    name = "chapter10_" + filename.removesuffix(".py")
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_streaming_emits_deltas_sources_and_end() -> None:
    module = load_example("01_streaming.py")

    class Responses:
        def create(self, **kwargs: object) -> list[SimpleNamespace]:
            assert kwargs["stream"] is True
            return [
                SimpleNamespace(type="response.output_text.delta", delta="Bonjour"),
                SimpleNamespace(type="response.completed"),
            ]

    client = SimpleNamespace(responses=Responses())
    passages = [module.Passage("Retour sous 30 jours.", "retours.md", 2)]
    events = list(module.evenements_sse("Quel délai ?", passages, model="test", client=client))

    assert "Bonjour" in events[0]
    assert "retours.md" in events[-2]
    assert events[-1] == "data: [FIN]\n\n"


def test_semantic_cache_hit_expiration_and_lru() -> None:
    module = load_example("02_cache_semantique.py")
    now = [100.0]

    class Encoder:
        def encode(self, text: str) -> list[float]:
            return [1.0, 0.0] if "retour" in text else [0.0, 1.0]

    cache = module.CacheSemantique(
        Encoder(), seuil=0.9, duree_vie=10, taille_max=1, horloge=lambda: now[0]
    )
    cache.enregistrer("retour", "30 jours")
    assert cache.chercher("retour produit") == "30 jours"
    cache.enregistrer("livraison", "5 jours")
    assert list(cache.entrees) == ["livraison"]
    now[0] = 111.0
    assert cache.chercher("livraison") is None


def test_token_pruning_uses_injected_scorer() -> None:
    module = load_example("03_token_pruning.py")
    pruner = module.TokenPruner(
        0.5,
        scorer=lambda sentence, question: 1.0 if "retour" in sentence.lower() else 0.0,
    )
    result = pruner.prune_context(
        "Les retours durent 30 jours. La livraison est gratuite.",
        "Quel délai de retour ?",
    )
    assert result == "Les retours durent 30 jours."


def test_only_long_chunks_are_summarized() -> None:
    module = load_example("04_summarize_chunks.py")
    prompts: list[str] = []

    def summarize(prompt: str) -> str:
        prompts.append(prompt)
        return "résumé"

    result = module.resumer_chunks(["court", "x" * 100], summarize, seuil_tokens=10)
    assert result == ["court", "résumé"]
    assert len(prompts) == 1


def test_economic_router_prioritizes_complex_and_critical_questions(monkeypatch) -> None:
    module = load_example("05_routeur_economique.py")
    assert module.classer("Quel est le délai ?") is module.Complexite.SIMPLE
    assert module.classer("Compare les politiques") is module.Complexite.COMPLEXE
    assert module.classer("Quel contrat appliquer ?") is module.Complexite.COMPLEXE
    assert module.classer("Explique cette procédure") is module.Complexite.MOYENNE

    monkeypatch.setenv("OPENAI_SMALL_MODEL", "petit")
    monkeypatch.setenv("OPENAI_LARGE_MODEL", "grand")
    assert module.modele_pour(module.Complexite.SIMPLE) == "petit"
    assert module.modele_pour(module.Complexite.COMPLEXE) == "grand"


def test_batch_embedding_retries_and_preserves_order() -> None:
    module = load_example("06_batch_embedding.py")

    class FlakyEncoder:
        def __init__(self) -> None:
            self.calls = 0

        def embed(self, texts: list[str]) -> list[list[float]]:
            self.calls += 1
            if self.calls == 1:
                raise TimeoutError("temporaire")
            return [[float(len(text))] for text in texts]

    encoder = FlakyEncoder()
    waits: list[float] = []
    vectors = module.vectoriser_lot(
        ["a", "bb"],
        encoder,
        attente_initiale=0.5,
        exceptions_reessayables=(TimeoutError,),
        dormir=waits.append,
    )
    assert vectors == [[1.0], [2.0]]
    assert waits == [0.5]

    assert module.vectoriser_corpus([], encoder, dormir=waits.append) == []
    with pytest.raises(ValueError):
        module.vectoriser_corpus(["x"], encoder, taille_lot=0)
