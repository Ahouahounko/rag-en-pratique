def tester_ancrage(jeu: list, systeme, corpus_etranger: list,
                   juge, seuil_similarite: float = 0.75) -> dict:
    """Le systeme utilise-t-il reellement ses passages ?

    corpus_etranger : passages d'un TOUT AUTRE domaine. Pas des
    passages voisins : on veut une absence totale de rapport,
    pour qu'aucune reponse ne puisse en etre tiree.
    """
    identiques, abstentions, total = 0, 0, 0

    for entree in jeu:
        question = entree["question"]

        reponse_reelle = systeme.repondre(question)["reponse"]
        reponse_substituee = systeme.generer_avec(
            question, contexte=echantillon(corpus_etranger, 5))

        if est_une_abstention(reponse_substituee):
            abstentions += 1          # comportement ATTENDU
        elif similarite(reponse_reelle,
                        reponse_substituee) > seuil_similarite:
            identiques += 1           # le contexte n'a rien change
        total += 1

    return {
        # Le bon score : la part de cas ou le systeme s'abstient
        # une fois prive de contexte utile.
        "taux_abstention": round(abstentions / total, 3),
        # Le mauvais : la part de reponses inchangees malgre un
        # contexte totalement etranger.
        "taux_reponse_de_memoire": round(identiques / total, 3),
        "ancrage_suffisant": abstentions / total > 0.85,
    }
