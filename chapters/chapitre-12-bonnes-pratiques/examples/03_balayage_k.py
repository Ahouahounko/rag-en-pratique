def balayer_k(questions: list[dict], retriever,
             valeurs_k: list[int] = None) -> list[dict]:
    """Mesure le rappel du contexte pour plusieurs valeurs de k.

    questions : [{"texte": "...", "passages_attendus": {"id1", ...}}]
    Retourne une liste triee par k croissant, prete a tracer.
    """
    if valeurs_k is None:
        valeurs_k = [1, 3, 5, 10, 15, 20]

    resultats = []

    for k in valeurs_k:
        rappels = []

        for question in questions:
            recuperes = retriever.chercher(question["texte"], k=k)
            ids_recuperes = {p.id for p in recuperes}
            attendus = question["passages_attendus"]

            # Rappel pour CETTE question : part des passages
            # attendus qui figurent bien parmi les k recuperes.
            trouves = ids_recuperes & attendus
            rappels.append(len(trouves) / len(attendus))

        rappel_moyen = sum(rappels) / len(rappels)
        resultats.append({"k": k, "rappel": round(rappel_moyen, 3)})

    return resultats


# Lecture du resultat : chercher le "coude" de la courbe, le
# point ou ajouter un candidat de plus n'ameliore quasiment plus
# le rappel. C'est ce point, pas un k choisi par habitude, qui
# doit fixer votre configuration de depart.
#
# k= 1 : rappel 0.412
# k= 3 : rappel 0.681
# k= 5 : rappel 0.774   <- le coude est ici
# k=10 : rappel 0.809
# k=15 : rappel 0.818
# k=20 : rappel 0.821
