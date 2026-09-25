def formater_avec_pertinence(passages: list, scores: list,
                             seuil: float = 0.5) -> str:
    """Annonce au modele la fiabilite relative de chaque extrait.

    Les scores bruts sont volontairement convertis en trois
    niveaux : un ecart de 0.02 n'a aucune signification, mais
    le modele le traiterait comme un classement.
    """
    blocs = []

    for passage, score in zip(passages, scores):
        if score < seuil:
            continue                    # sous le seuil : on ecarte

        if score >= 0.85:
            niveau = "correspondance forte"
        elif score >= 0.70:
            niveau = "correspondance moyenne"
        else:
            niveau = "correspondance faible - a confirmer"

        numero = len(blocs) + 1
        source = passage.metadata.get("source", "inconnu")

        blocs.append(
            f"[doc_{numero}] {source} ({niveau})\n"
            f"{passage.page_content}"
        )

    if not blocs:
        # Cas important : mieux vaut le dire explicitement au
        # modele que lui envoyer un contexte vide, qu'il
        # comblerait avec sa memoire.
        return "Aucun extrait ne depasse le seuil de pertinence."

    return "\n\n---\n\n".join(blocs)
