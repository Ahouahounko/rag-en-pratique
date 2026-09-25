import statistics


def diagnostiquer(moyennes: dict, seuils: dict = None) -> str:
    """Traduit les scores en un diagnostic actionnable.

    C'est la table des configurations, transcrite. La valeur
    ajoutee n'est pas le calcul : c'est de refuser de rendre
    des nombres sans conclusion.
    """
    s = seuils or {"faithfulness": 0.80, "answer_relevance": 0.75,
                   "contextual_precision": 0.65,
                   "contextual_recall": 0.70}

    bas = {nom for nom, seuil in s.items()
           if moyennes.get(nom, 0) < seuil}

    if not bas:
        return "Systeme sain. Surveiller sans intervenir."

    # --- Les trois combinaisons canoniques, en premier ---
    if ("faithfulness" in bas
            and "answer_relevance" not in bas):
        return ("Hallucination a la generation : la reponse est "
                "alignee sur la question mais non etayee. "
                "Renforcer l'ancrage du prompt.")

    if ("answer_relevance" in bas
            and "contextual_recall" not in bas):
        return ("Echec a la generation : le contexte contenait le "
                "necessaire. Revoir prompt, format ou modele.")

    if {"contextual_precision", "contextual_recall"} <= bas:
        return ("Echec au retrieval : contexte faux ET insuffisant. "
                "Verifier A LA MAIN si l'information existe dans "
                "le corpus avant d'optimiser le retriever.")

    # --- Cas simples restants ---
    if bas == {"contextual_precision"}:
        return "Retriever bruyant : re-ranking, reduire k, seuil."
    if bas == {"contextual_recall"}:
        return "Retriever incomplet : hybride, augmenter k, decoupage."
    if len(bas) >= 3:
        return "Defaut systemique : reprendre depuis l'ingestion."

    return f"Configuration mixte, metriques basses : {sorted(bas)}"


def lancer_campagne(jeu: list, systeme, juge,
                    metadonnees: dict) -> dict:
    """Execute le jeu de reference et produit un rapport complet.

    metadonnees : outil, version, modele juge, version du jeu.
    Sans ces quatre informations, le rapport sera inexploitable
    dans six mois (cf. partie D sur la comparabilite des scores).
    """
    par_metrique = {"faithfulness": [], "answer_relevance": [],
                    "contextual_precision": [], "contextual_recall": []}
    par_cas = []

    for cas in jeu:
        sortie = systeme.repondre(cas["question"])
        contexte = "\n\n".join(p.texte for p in sortie["sources"])

        scores = {
            "faithfulness": calculer_faithfulness(
                sortie["reponse"], contexte, juge)["score"],
            "answer_relevance": mesurer_answer_relevance(
                cas["question"], sortie["reponse"], juge),
            "contextual_precision": mesurer_contextual_precision(
                cas["question"], sortie["sources"], juge),
            "contextual_recall": mesurer_contextual_recall(
                cas["passages_attendus"], sortie["sources"]),
        }

        for nom, valeur in scores.items():
            par_metrique[nom].append(valeur)

        # On conserve le detail par cas : c'est lui qui permettra
        # la ventilation par segment (fairness) et le diagnostic.
        par_cas.append({**scores, "question": cas["question"],
                        "type": cas.get("type"),
                        "sujet": cas.get("sujet")})

    moyennes = {nom: round(statistics.mean(v), 3)
                for nom, v in par_metrique.items() if v}

    return {"moyennes": moyennes,
            "diagnostic": diagnostiquer(moyennes),
            "par_cas": par_cas,
            "metadonnees": metadonnees}
