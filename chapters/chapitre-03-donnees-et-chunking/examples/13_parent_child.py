import uuid

# --- A l'ingestion -------------------------------------------------

def indexer_parent_child(document: str, vector_store, docstore: dict) -> None:
    """
    Deux niveaux : les PARENTS vivent dans un magasin cle-valeur,
    seuls les ENFANTS sont vectorises et cherchables.
    """
    parents = decoupage_fixe(document, taille=1024, overlap=100)

    for parent_texte in parents:
        id_parent = str(uuid.uuid4())
        docstore[id_parent] = parent_texte          # simple dict ou Redis

        enfants = decoupage_fixe(parent_texte, taille=256, overlap=30)
        for enfant_texte in enfants:
            vector_store.ajouter(
                vecteur=embarquer(enfant_texte),
                texte=enfant_texte,
                metadonnees={"id_parent": id_parent},
            )


# --- A la requete ----------------------------------------------------

def recuperer_avec_parents(requete: str, vector_store, docstore: dict,
                           k: int = 8) -> list[str]:
    """
    Cherche parmi les enfants (precision), renvoie les parents (contexte).
    Le passage par un set est essentiel : plusieurs enfants d'un meme
    parent ne doivent renvoyer ce parent qu'une seule fois, sans quoi
    on gaspille la fenetre de contexte en doublons.
    """
    enfants_trouves = vector_store.recherche(requete, k=k)
    ids_parents = {e.metadonnees["id_parent"] for e in enfants_trouves}
    return [docstore[i] for i in ids_parents]
