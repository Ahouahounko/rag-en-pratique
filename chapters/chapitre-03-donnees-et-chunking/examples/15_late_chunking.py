import numpy as np

def late_chunking(document: str,
                  modele_long_contexte,
                  frontieres: list[tuple[int, int]]) -> list[np.ndarray]:
    """
    Args:
        document           : le document complet, non decoupe
        modele_long_contexte : modele capable de traiter tout le document
        frontieres         : liste de (token_debut, token_fin)

    Retour : un vecteur par chunk, chacun contextualise globalement.
    """
    # Etape 1 : embedding du document ENTIER.
    # L'attention s'applique sur toute la sequence, donc chaque
    # vecteur de token "a vu" le reste du document.
    vecteurs_tokens = modele_long_contexte.encode_tokens(document)
    # forme : [n_tokens, dimension]

    # Etape 2 : le decoupage intervient APRES, au niveau des vecteurs.
    vecteurs_chunks = []
    for debut, fin in frontieres:
        # Mean pooling sur des tokens deja contextualises
        vecteurs_chunks.append(vecteurs_tokens[debut:fin].mean(axis=0))

    return vecteurs_chunks


def frontieres_en_tokens(document: str, chunk_size_chars: int,
                         tokenizer) -> list[tuple[int, int]]:
    """
    Convertit des frontieres de chunks CARACTERES (celles que votre
    splitter habituel produit) en frontieres TOKENS, requises par
    late_chunking(). C'est l'etape qui manque dans la plupart des
    exemples publies, et qui bloque une premiere integration.
    """
    frontieres = []
    for debut_c in range(0, len(document), chunk_size_chars):
        fin_c = min(debut_c + chunk_size_chars, len(document))
        debut_t = len(tokenizer.encode(document[:debut_c]))
        fin_t = len(tokenizer.encode(document[:fin_c]))
        frontieres.append((debut_t, fin_t))
    return frontieres


# --- Exemple d'utilisation, de bout en bout -------------------------
#
# frontieres = frontieres_en_tokens(document, chunk_size_chars=2000,
#                                    tokenizer=modele_long_contexte.tokenizer)
# vecteurs   = late_chunking(document, modele_long_contexte, frontieres)
#
# for (debut, fin), vecteur in zip(frontieres, vecteurs):
#     texte_chunk = document[debut:fin]   # pour l'affichage / citation
#     vector_store.ajouter(vecteur=vecteur, texte=texte_chunk)
#
# La difference avec un pipeline standard tient en deux lignes :
#
#   STANDARD       texte_chunk = document[debut:fin]
#                  vecteur     = modele.encode(texte_chunk)
#                  -> le vecteur ne "voit" que le chunk
#
#   LATE CHUNKING  tokens  = modele.encode_tokens(document)
#                  vecteur = tokens[debut:fin].mean(axis=0)
#                  -> le vecteur porte le contexte du document entier
