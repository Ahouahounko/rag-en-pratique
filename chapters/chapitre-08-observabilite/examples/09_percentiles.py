import time
from collections import deque
import statistics


class SuiviLatence:
    """Percentiles glissants, etape par etape.

    On conserve les mesures INDIVIDUELLES : une moyenne cumulee
    ne permet pas de reconstituer un percentile. C'est l'erreur
    d'instrumentation la plus courante, et elle est irreversible.
    """

    def __init__(self, fenetre: int = 1000):
        # deque bornee : les mesures les plus anciennes sortent
        # automatiquement, la memoire reste constante.
        self.mesures = {etape: deque(maxlen=fenetre)
                        for etape in ("vectorisation", "recherche",
                                      "reclassement", "generation",
                                      "total")}

    def chronometrer(self, etape: str):
        """Context manager : with suivi.chronometrer("recherche"):"""
        return _Chrono(self.mesures[etape])

    def percentiles(self) -> dict:
        rapport = {}
        for etape, valeurs in self.mesures.items():
            if len(valeurs) < 20:      # trop peu pour un percentile
                continue
            triees = sorted(valeurs)
            rapport[etape] = {
                "p50": round(statistics.median(triees), 1),
                "p95": round(triees[int(len(triees) * 0.95)], 1),
                "p99": round(triees[int(len(triees) * 0.99)], 1),
                "n": len(triees),
            }
        return rapport

    def part_de_chaque_etape(self) -> dict:
        """Ou passe le temps ? Repond avant d'optimiser au hasard."""
        p = self.percentiles()
        total = p.get("total", {}).get("p50")
        if not total:
            return {}
        return {etape: f"{v['p50'] / total * 100:.0f} %"
                for etape, v in p.items() if etape != "total"}


class _Chrono:
    def __init__(self, cible): self.cible = cible
    def __enter__(self): self.debut = time.perf_counter(); return self
    def __exit__(self, *_):
        self.cible.append((time.perf_counter() - self.debut) * 1000)
