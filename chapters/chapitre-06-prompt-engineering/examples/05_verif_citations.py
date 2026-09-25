import re


def verifier_citations(reponse: str, passages: list) -> dict:
    """Controle que les citations renvoient a des extraits reels.

    Ne verifie PAS que l'extrait etaye l'affirmation - cela
    demande un modele (cf. chapitre 8). Verifie seulement que
    l'identifiant existe et que la reponse n'est pas orpheline.
    """
    cites = set(re.findall(r"\[doc_(\d+)\]", reponse))
    disponibles = {str(i) for i in range(1, len(passages) + 1)}

    inventees = cites - disponibles      # citation d'un doc absent
    inutilisees = disponibles - cites    # extrait fourni jamais cite

    # Une affirmation est une phrase qui n'est ni une question
    # ni la formule de refus.
    phrases = [p.strip() for p in re.split(r"[.!?]\s+", reponse)
               if len(p.strip()) > 30]
    sans_source = [p for p in phrases if "[doc_" not in p]

    return {
        "citations_inventees": sorted(inventees),
        "extraits_non_cites": sorted(inutilisees),
        "phrases_sans_source": len(sans_source),
        "conforme": not inventees and not sans_source,
    }
