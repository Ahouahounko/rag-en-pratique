def decoupage_fixe(texte: str, taille: int = 512,
                   overlap: int = 50) -> list[str]:
    # Coupe tous les N tokens. Aucune intelligence, et c'est voulu :
    # c'est la reference contre laquelle tout le reste se mesure.
    tokens = encoder.encode(texte)
    pas = taille - overlap
    chunks = []

    for debut in range(0, len(tokens), pas):
        fenetre = tokens[debut : debut + taille]
        chunks.append(encoder.decode(fenetre))
        if debut + taille >= len(tokens):
            break

    return chunks
