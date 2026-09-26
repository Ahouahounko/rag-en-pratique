"""Assignation stable et analyse d'une expérience A/B RAG."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from scipy import stats


def assigner_variante(identifiant_utilisateur: str, graine: str = "test-embedding-v2") -> str:
    if not identifiant_utilisateur or not graine:
        raise ValueError("identifiant_utilisateur et graine sont obligatoires")
    digest = hashlib.sha256(f"{graine}:{identifiant_utilisateur}".encode()).digest()
    return "A" if int.from_bytes(digest[:8], "big") % 2 == 0 else "B"


@dataclass
class ResultatsTest:
    scores_a: list[float] = field(default_factory=list)
    scores_b: list[float] = field(default_factory=list)

    def effectif_atteint(self, effectif_requis: int) -> bool:
        if effectif_requis <= 1:
            raise ValueError("effectif_requis doit être supérieur à 1")
        return len(self.scores_a) >= effectif_requis and len(self.scores_b) >= effectif_requis

    def analyser(
        self,
        *,
        alpha: float = 0.05,
        effet_minimal: float = 0.0,
    ) -> dict[str, float | bool | str]:
        if len(self.scores_a) < 2 or len(self.scores_b) < 2:
            raise ValueError("Chaque variante doit contenir au moins deux observations")
        if not 0 < alpha < 1 or effet_minimal < 0:
            raise ValueError("alpha et effet_minimal sont invalides")

        moyenne_a = sum(self.scores_a) / len(self.scores_a)
        moyenne_b = sum(self.scores_b) / len(self.scores_b)
        delta = moyenne_b - moyenne_a
        _, p_value = stats.ttest_ind(self.scores_a, self.scores_b, equal_var=False)
        significant = bool(p_value < alpha)
        useful = abs(delta) >= effet_minimal
        decision = "B" if significant and useful and delta > 0 else "A" if significant and useful else "inconcluant"
        return {
            "moyenne_a": moyenne_a,
            "moyenne_b": moyenne_b,
            "delta": delta,
            "p_valeur": float(p_value),
            "significatif": significant,
            "effet_utile": useful,
            "decision": decision,
        }


if __name__ == "__main__":
    test = ResultatsTest([0.70, 0.71, 0.69, 0.72], [0.80, 0.82, 0.79, 0.81])
    print(test.analyser(effet_minimal=0.02))
