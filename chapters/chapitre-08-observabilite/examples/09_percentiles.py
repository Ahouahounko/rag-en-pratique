"""Suivre des percentiles glissants de latence, étape par étape."""

from __future__ import annotations

import math
import statistics
import time
from collections import deque

ETAPES = ("vectorisation", "recherche", "reclassement", "generation", "total")


def percentile(valeurs: list[float], quantile: float) -> float:
    if not valeurs:
        raise ValueError("Aucune mesure")
    if not 0 < quantile <= 1:
        raise ValueError("Le quantile doit appartenir à ]0, 1]")
    triees = sorted(valeurs)
    return triees[math.ceil(quantile * len(triees)) - 1]


class SuiviLatence:
    def __init__(self, fenetre: int = 1000, minimum: int = 20) -> None:
        if fenetre <= 0 or minimum <= 0:
            raise ValueError("fenetre et minimum doivent être positifs")
        self.minimum = minimum
        self.mesures = {etape: deque(maxlen=fenetre) for etape in ETAPES}

    def chronometrer(self, etape: str):
        if etape not in self.mesures:
            raise KeyError(f"Étape inconnue : {etape}")
        return _Chrono(self.mesures[etape])

    def enregistrer(self, etape: str, millisecondes: float) -> None:
        if millisecondes < 0:
            raise ValueError("Une latence ne peut pas être négative")
        self.mesures[etape].append(float(millisecondes))

    def percentiles(self) -> dict[str, dict[str, float | int]]:
        rapport = {}
        for etape, valeurs in self.mesures.items():
            if len(valeurs) < self.minimum:
                continue
            liste = list(valeurs)
            rapport[etape] = {
                "p50": round(statistics.median(liste), 1),
                "p95": round(percentile(liste, 0.95), 1),
                "p99": round(percentile(liste, 0.99), 1),
                "n": len(liste),
            }
        return rapport

    def part_de_chaque_etape(self) -> dict[str, str]:
        rapport = self.percentiles()
        total = rapport.get("total", {}).get("p50")
        if not total:
            return {}
        return {
            etape: f"{float(valeurs['p50']) / float(total) * 100:.0f} %"
            for etape, valeurs in rapport.items()
            if etape != "total"
        }


class _Chrono:
    def __init__(self, cible: deque) -> None:
        self.cible = cible
        self.debut = 0.0

    def __enter__(self):
        self.debut = time.perf_counter()
        return self

    def __exit__(self, *_: object) -> None:
        self.cible.append((time.perf_counter() - self.debut) * 1000)


if __name__ == "__main__":
    suivi = SuiviLatence(minimum=5)
    for valeur in [10, 12, 14, 18, 40]:
        suivi.enregistrer("recherche", valeur)
    print(suivi.percentiles())
