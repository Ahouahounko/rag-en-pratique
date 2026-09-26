"""Réduction du contexte par score de pertinence phrase-question."""

from __future__ import annotations

import re
from collections.abc import Callable

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


class TokenPruner:
    def __init__(
        self,
        threshold: float = 0.3,
        *,
        scorer: Callable[[str, str], float] | None = None,
        model: str = "facebook/bart-large-mnli",
    ) -> None:
        if not 0 <= threshold <= 1:
            raise ValueError("threshold doit être compris entre 0 et 1")
        self.threshold = threshold
        self.scorer = scorer or self._huggingface_scorer(model)

    @staticmethod
    def _huggingface_scorer(model: str) -> Callable[[str, str], float]:
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError('Installez les modèles avec pip install -e ".[huggingface]"') from exc
        classifier = pipeline("zero-shot-classification", model=model)

        def score(sentence: str, question: str) -> float:
            result = classifier(sentence, [question], multi_label=True)
            return float(result["scores"][0])

        return score

    def prune_context(self, context: str, question: str) -> str:
        sentences = [item.strip() for item in SENTENCE_BOUNDARY.split(context) if item.strip()]
        retained = [
            sentence
            for sentence in sentences
            if self.scorer(sentence, question) >= self.threshold
        ]
        return " ".join(retained)


if __name__ == "__main__":
    def score_demo(sentence: str, question: str) -> float:
        words = set(question.lower().split())
        return len(words & set(sentence.lower().split())) / max(len(words), 1)

    pruner = TokenPruner(0.1, scorer=score_demo)
    print(pruner.prune_context("Retours sous 30 jours. Livraison gratuite.", "délai retours"))
