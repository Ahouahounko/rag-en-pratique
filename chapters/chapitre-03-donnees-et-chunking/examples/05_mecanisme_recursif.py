"""Version exécutable du mécanisme récursif présenté en pseudo-code."""


def decouper_recursivement(
    texte: str,
    separateurs: list[str],
    budget: int,
) -> list[str]:
    """Découpe du séparateur le plus structurant au moins structurant."""

    if len(texte) <= budget:
        return [texte.strip()] if texte.strip() else []
    if not separateurs:
        return [texte[index : index + budget] for index in range(0, len(texte), budget)]

    separateur, *restants = separateurs
    morceaux = texte.split(separateur) if separateur else list(texte)
    resultat: list[str] = []
    courant = ""
    for morceau in morceaux:
        candidat = f"{courant}{separateur if courant else ''}{morceau}"
        if len(candidat) <= budget:
            courant = candidat
            continue
        if courant:
            resultat.append(courant.strip())
        if len(morceau) <= budget:
            courant = morceau
        else:
            resultat.extend(decouper_recursivement(morceau, restants, budget))
            courant = ""
    if courant.strip():
        resultat.append(courant.strip())
    return resultat


if __name__ == "__main__":
    document = "Titre\n\nPremier paragraphe assez long.\n\nDeuxième paragraphe détaillé."
    print(decouper_recursivement(document, ["\n\n", ". ", " ", ""], budget=35))
