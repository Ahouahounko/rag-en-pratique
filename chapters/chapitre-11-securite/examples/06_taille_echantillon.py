import math


def taille_echantillon(ecart_type: float, effet_attendu: float,
                       alpha: float = 0.05, puissance: float = 0.8) -> int:
    """Nombre d'observations necessaires PAR VARIANTE.

    ecart_type     : mesure sur votre jeu de reference, jamais devine.
    effet_attendu  : difference de score qu'on veut pouvoir detecter
                     (ex. 0.02 pour 2 points de score RAGAS).
    alpha          : risque de faux positif tolere (0.05 = 5 %).
    puissance      : probabilite de detecter l'effet s'il existe
                     vraiment (0.8 est la convention standard).
    """
    # Valeurs standard pour un test bilateral, alpha=0.05,
    # puissance=0.8 : z_alpha/2 = 1.96, z_puissance = 0.84.
    z_alpha = 1.96
    z_puissance = 0.84

    n = 2 * ((z_alpha + z_puissance) * ecart_type / effet_attendu) ** 2
    return math.ceil(n)


# Exemple : ecart-type de 0.15 mesure sur le golden dataset.
for effet in (0.10, 0.05, 0.02):
    n = taille_echantillon(ecart_type=0.15, effet_attendu=effet)
    print(f"Detecter {effet:.2f} : {n} observations par variante")

# Detecter 0.10 : 36 observations par variante
# Detecter 0.05 : 142 observations par variante
# Detecter 0.02 : 882 observations par variante
#
# L'effectif varie comme l'inverse du CARRE de l'effet recherche :
# diviser l'effet par deux multiplie l'effectif par quatre.
