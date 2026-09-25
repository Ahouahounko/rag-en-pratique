import numpy as np

def chunking_semantique(texte: str,
                        modele_embedding,
                        percentile: int = 95) -> list[str]:
    """
    Decoupe un texte aux endroits ou le sujet change.

    1. Segmenter en phrases
    2. Vectoriser chaque phrase (une seule passe, par lot)
    3. Mesurer la distance entre phrases consecutives
    4. Couper aux distances du percentile choisi

    Le percentile (95 par defaut) s'adapte au document :
    plus bas  -> plus de coupures, chunks plus fins
    plus haut -> moins de coupures, chunks plus larges
    """
    phrases = [p.strip() for p in texte.split(".") if len(p.strip()) > 20]
    if len(phrases) < 2:
        return [texte]

    vecteurs = np.array(modele_embedding.embed_documents(phrases))

    # Distance cosinus entre chaque phrase et la precedente
    normes = np.linalg.norm(vecteurs, axis=1, keepdims=True) + 1e-8
    unitaires = vecteurs / normes
    similarites = np.sum(unitaires[1:] * unitaires[:-1], axis=1)
    distances = 1.0 - similarites

    # Le seuil n'est pas fixe : il est relatif a CE document
    seuil = np.percentile(distances, percentile)

    chunks, courant = [], [phrases[0]]
    for i, d in enumerate(distances, start=1):
        if d >= seuil:
            chunks.append(". ".join(courant) + ".")
            courant = [phrases[i]]
        else:
            courant.append(phrases[i])

    if courant:
        chunks.append(". ".join(courant) + ".")

    return chunks
