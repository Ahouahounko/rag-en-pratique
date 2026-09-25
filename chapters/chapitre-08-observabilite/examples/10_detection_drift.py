import numpy as np
from scipy.stats import ks_2samp


def detecter_derive(reference: dict[str, list[float]],
                    actuel: dict[str, list[float]],
                    seuil_p: float = 0.05,
                    seuil_ecart: float = 0.05) -> list[dict]:
    """Compare les distributions actuelles a une reference.

    DEUX conditions doivent etre reunies pour alerter :
      - significativite statistique (test KS)
      - ampleur suffisante (ecart de moyenne)

    La seconde evite le piege classique : sur de gros volumes,
    le test KS devient significatif pour des ecarts infimes,
    sans aucune portee pratique. Une alerte quotidienne pour
    un dixieme de point finit toujours par etre ignoree.
    """
    alertes = []

    for metrique, valeurs_actuelles in actuel.items():
        valeurs_ref = reference.get(metrique)
        if not valeurs_ref or not valeurs_actuelles:
            continue

        _, p_valeur = ks_2samp(valeurs_ref, valeurs_actuelles)

        moyenne_ref = float(np.mean(valeurs_ref))
        moyenne_act = float(np.mean(valeurs_actuelles))
        ecart = moyenne_act - moyenne_ref

        if p_valeur < seuil_p and abs(ecart) > seuil_ecart:
            alertes.append({
                "metrique": metrique,
                "reference": round(moyenne_ref, 3),
                "actuel": round(moyenne_act, 3),
                "ecart_points": round(ecart * 100, 1),
                "p_valeur": round(p_valeur, 4),
                "sens": "degradation" if ecart < 0 else "amelioration",
            })

    return alertes
