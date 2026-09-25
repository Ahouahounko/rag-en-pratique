def generer_question_discriminante(passage_cible, index, modele,
                                   n_distracteurs: int = 2) -> dict:
    """Fabrique une question que seul le passage cible resout.

    Les distracteurs viennent de VOTRE index : ce sont les
    passages que votre retriever juge deja proches de la cible,
    donc ceux qu'il risque reellement de confondre avec elle.
    """
    # Les voisins les plus proches, la cible exclue
    voisins = [p for p in index.chercher(passage_cible.texte,
                                         k=n_distracteurs + 1)
               if p.id != passage_cible.id][:n_distracteurs]

    textes_distracteurs = "\n\n".join(
        f"[Distracteur {i}] {p.texte}"
        for i, p in enumerate(voisins, start=1)
    )

    sortie = modele.invoke(f"""PASSAGE CIBLE :
{passage_cible.texte}

PASSAGES VOISINS (ils ne contiennent PAS la reponse) :
{textes_distracteurs}

Ecris une question qui remplit TOUTES ces conditions :
- seul le PASSAGE CIBLE permet d'y repondre ;
- elle reprend du vocabulaire ou des themes des VOISINS ;
- elle ne cite pas le passage cible mot pour mot ;
- un utilisateur reel pourrait la poser.

Reponds en JSON : {{"question": "...", "reponse": "..."}}""").content

    resultat = extraire_json(sortie)
    return {
        **resultat,
        "passages_attendus": [passage_cible.id],
        # On conserve les distracteurs : s'ils remontent devant la
        # cible, on sait exactement ce que le retriever a confondu.
        "distracteurs_connus": [p.id for p in voisins],
        "type": "discriminante",
    }
