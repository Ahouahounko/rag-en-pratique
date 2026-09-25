def fusionner_chunks_voisins(chunks: list[dict]) -> str:
    """
    Recolle en un passage continu les chunks qui se chevauchent.

    Chaque chunk porte ses offsets dans le document source
    (start_pos / end_pos) : c'est ce qui rend la fusion possible.
    Sans ces metadonnees, on ne peut que dedupliquer approximativement.
    """
    if not chunks:
        return ""

    # 1. Remettre les fragments dans l'ordre du document d'origine
    #    (le retrieval les a renvoyes par score, pas par position)
    ordonnes = sorted(chunks, key=lambda c: c["start_pos"])

    morceaux = [ordonnes[0]["text"]]
    fin_courante = ordonnes[0]["end_pos"]

    for chunk in ordonnes[1:]:
        if chunk["start_pos"] < fin_courante:
            # Chevauchement : on n'ajoute que la partie inedite
            debut_utile = fin_courante - chunk["start_pos"]
            morceaux.append(chunk["text"][debut_utile:])
        else:
            # Chunks disjoints : marqueur de discontinuite explicite
            morceaux.append("\n[...]\n" + chunk["text"])

        fin_courante = max(fin_courante, chunk["end_pos"])

    return " ".join(morceaux)
