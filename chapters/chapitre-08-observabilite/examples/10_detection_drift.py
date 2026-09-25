"""Détecter une dérive statistiquement significative et matériellement importante."""

from __future__ import annotations

import numpy as np
from scipy.stats import ks_2samp


def detecter_derive(
    reference: dict[str, list[float]],
    actuel: dict[str, list[float]],
    seuil_p: float = 0.05,
    seuil_ecart: float = 0.05,
    *,
    plus_grand_est_meilleur: dict[str, bool] | None = None,
) -> list[dict[str, object]]:
    directions = plus_grand_est_meilleur or {}
    alertes = []
    for metrique, valeurs_actuelles in actuel.items():
        valeurs_ref = reference.get(metrique)
        if not valeurs_ref or not valeurs_actuelles:
            continue
        _, p_valeur = ks_2samp(valeurs_ref, valeurs_actuelles)
        moyenne_ref = float(np.mean(valeurs_ref))
        moyenne_actuelle = float(np.mean(valeurs_actuelles))
        ecart = moyenne_actuelle - moyenne_ref
        if p_valeur >= seuil_p or abs(ecart) <= seuil_ecart:
            continue
        hausse_souhaitable = directions.get(metrique, True)
        degradation = ecart < 0 if hausse_souhaitable else ecart > 0
        alertes.append(
            {
                "metrique": metrique,
                "reference": round(moyenne_ref, 3),
                "actuel": round(moyenne_actuelle, 3),
                "ecart_points": round(ecart * 100, 1),
                "p_valeur": round(float(p_valeur), 4),
                "sens": "degradation" if degradation else "amelioration",
            }
        )
    return alertes


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    reference = {"faithfulness": rng.normal(0.90, 0.02, 200).tolist()}
    actuel = {"faithfulness": rng.normal(0.75, 0.02, 200).tolist()}
    print(detecter_derive(reference, actuel))
