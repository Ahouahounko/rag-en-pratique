from collections import Counter


def attribuer_defaillances(jeu: list, systeme, juge) -> dict:
    """Croise succes du retrieval et exactitude de la reponse.

    Produit les quatre cas de la matrice, plus la liste des
    questions concernees : c'est cette liste que l'on ouvre
    ensuite pour comprendre, pas le compteur.
    """
    cas = Counter()
    exemples = {"generateur": [], "retriever": [],
                "ancrage": [], "nominal": []}

    for entree in jeu:
        sortie = systeme.repondre(entree["question"])

        # --- Verdict 1 : le retrieval, SANS modele ---
        # Simple test d'appartenance sur des identifiants.
        obtenus = {p.id for p in sortie["sources"]}
        attendus = set(entree["passages_attendus"])
        retrieval_ok = bool(attendus & obtenus)

        # --- Verdict 2 : la reponse, comparee a la reference ---
        reponse_ok = juge_exactitude(
            question=entree["question"],
            reponse=sortie["reponse"],
            reference=entree["reponse"],
            juge=juge,
        )

        if retrieval_ok and reponse_ok:
            categorie = "nominal"
        elif retrieval_ok and not reponse_ok:
            categorie = "generateur"     # le contexte etait bon
        elif not retrieval_ok and not reponse_ok:
            categorie = "retriever"      # le contexte manquait
        else:
            # Juste SANS les bons passages : le modele a repondu
            # de memoire. Compte comme un succes dans les
            # metriques de bout en bout, c'est pourtant un defaut.
            categorie = "ancrage"

        cas[categorie] += 1
        exemples[categorie].append(entree["question"])

    total = sum(cas.values())
    parts = {nom: round(n / total, 3) for nom, n in cas.items()}

    # Ou investir ? Le rapport entre les deux cas d'echec.
    priorite = ("retriever" if cas["retriever"] >= cas["generateur"]
                else "generateur")

    return {"repartition": parts, "priorite": priorite,
            "alerte_ancrage": parts.get("ancrage", 0) > 0.05,
            "exemples": exemples}
