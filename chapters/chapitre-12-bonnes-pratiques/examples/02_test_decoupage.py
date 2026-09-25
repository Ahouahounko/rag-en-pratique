def tester_decoupages(documents: list, questions: list[dict],
                      configurations: list[dict],
                      encodeur) -> list[dict]:
    """Compare plusieurs configurations de decoupage.

    questions : [{"texte": "...", "reponse_attendue": "..."}]
                La reponse attendue sert de sonde : on verifie
                qu'elle est CONTENUE dans un chunk recupere.
    configurations : [{"taille": 256, "recouvrement": 0}, ...]
    """
    resultats = []

    for config in configurations:
        chunks = decouper(documents, **config)
        index = indexer_en_memoire(chunks, encodeur)

        complets, partiels, manques = 0, 0, 0

        for question in questions:
            recuperes = index.chercher(question["texte"], k=5)
            attendu = question["reponse_attendue"].lower()

            # La reponse tient-elle ENTIERE dans un seul chunk ?
            if any(attendu in c.texte.lower() for c in recuperes):
                complets += 1
            # Sinon, est-elle eclatee sur plusieurs chunks
            # recuperes ? C'est le cas ambigu : le modele PEUT
            # recoller, mais il n'y arrive pas toujours.
            elif attendu in " ".join(c.texte.lower() for c in recuperes):
                partiels += 1
            else:
                manques += 1

        resultats.append({
            **config,
            "complet": complets / len(questions),
            "partiel": partiels / len(questions),
            "manque": manques / len(questions),
            "nb_chunks": len(chunks),
        })

    # On trie sur le taux COMPLET, pas sur complet + partiel :
    # une reponse eclatee sur trois chunks est un pari, pas un
    # succes.
    return sorted(resultats, key=lambda r: r["complet"], reverse=True)
