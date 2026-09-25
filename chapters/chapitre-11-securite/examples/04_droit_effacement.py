import logging

logger = logging.getLogger(__name__)


def effacer_personne(identifiant: str, registre, index,
                     cache, journaux) -> dict:
    """Supprime toute trace d'une personne, index compris.

    L'ordre compte : on purge le cache AVANT l'index. Sinon une
    requete arrivant entre les deux operations remettrait en
    cache une reponse construite sur des donnees en cours de
    suppression.
    """
    bilan = {"passages": 0, "entrees_cache": 0, "documents": 0}

    documents = registre.documents_mentionnant(identifiant)
    bilan["documents"] = len(documents)

    # 1. Cache : en premier, pour la raison ci-dessus.
    bilan["entrees_cache"] = cache.purger_si_source_dans(documents)

    # 2. Index vectoriel : suppression des passages concernes.
    for document in documents:
        identifiants = registre.passages_de(document)
        index.supprimer(identifiants)
        bilan["passages"] += len(identifiants)

    # 3. Registre : on retire les entrees devenues orphelines.
    registre.oublier(documents)

    # 4. Journaux applicatifs : souvent oublies, et pourtant ils
    #    contiennent les questions et les reponses, donc parfois
    #    les donnees elles-memes.
    journaux.anonymiser_occurrences(identifiant)

    logger.info("Effacement %s : %s", identifiant, bilan)
    return bilan
