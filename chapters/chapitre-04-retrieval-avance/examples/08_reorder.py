def reordonner_pour_le_prompt(chunks: list) -> list:
    """Place les chunks les plus pertinents aux deux extremites.

    Entree  : liste DEJA triee par pertinence decroissante.
    Sortie  : meme liste, disposee en V.

    Avec 6 chunks classes [1, 2, 3, 4, 5, 6] :
        ordre brut   -> 1 2 3 4 5 6   (le n.1 seul en bonne place)
        ordre en V   -> 1 3 5 6 4 2   (n.1 au debut, n.2 a la fin)

    Le principe : on distribue en alternance a gauche et a droite,
    puis on retourne la moitie droite. Les mieux classes se
    retrouvent aux bords, les moins bons au centre.
    """
    if len(chunks) <= 2:
        return chunks

    gauche, droite = [], []
    for position, chunk in enumerate(chunks):
        (gauche if position % 2 == 0 else droite).append(chunk)

    return gauche + droite[::-1]
