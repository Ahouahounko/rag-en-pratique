"""Calcul de l'effectif nécessaire par variante avant une expérience A/B."""

from __future__ import annotations

import math

from scipy.stats import norm


def taille_echantillon(
    ecart_type: float,
    effet_attendu: float,
    *,
    alpha: float = 0.05,
    puissance: float = 0.8,
) -> int:
    if ecart_type <= 0 or effet_attendu <= 0:
        raise ValueError("ecart_type et effet_attendu doivent être strictement positifs")
    if not 0 < alpha < 1 or not 0 < puissance < 1:
        raise ValueError("alpha et puissance doivent être compris entre 0 et 1")
    z_alpha = norm.ppf(1 - alpha / 2)
    z_power = norm.ppf(puissance)
    size = 2 * ((z_alpha + z_power) * ecart_type / effet_attendu) ** 2
    return math.ceil(size)


if __name__ == "__main__":
    for effect in (0.10, 0.05, 0.02):
        size = taille_echantillon(ecart_type=0.15, effet_attendu=effect)
        print(f"Détecter {effect:.2f} : {size} observations par variante")
