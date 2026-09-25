def calculer_faithfulness(reponse: str, contexte: str, juge) -> dict:
    """Decompose la reponse, puis verifie chaque affirmation.

    Les deux etapes sont VOLONTAIREMENT separees : c'est ce qui
    rend le resultat auditable. Un score de 0.67 sans le detail
    des affirmations n'apprend rien ; avec le detail, on voit
    immediatement CE QUI a ete invente.
    """
    # --- Etape 1 : decomposer en affirmations elementaires ---
    brut = juge.invoke(f"""Decompose ce texte en affirmations
elementaires, une par ligne, sans numerotation.
Une affirmation = un fait verifiable et un seul.
Ne reformule pas, n'ajoute rien, n'interprete pas.

Texte : {reponse}

Affirmations :""").content

    affirmations = [ligne.strip("- ").strip()
                    for ligne in brut.split("\n") if ligne.strip()]

    if not affirmations:
        return {"score": 1.0, "detail": [], "total": 0}

    # --- Etape 2 : verifier chacune contre les passages ---
    # ATTENTION : le critere retenu ici est "peut etre DEDUITE du
    # contexte". C'est le critere de RAGAS. D'autres outils
    # retiennent "n'est pas CONTREDITE par le contexte", ce qui
    # est bien plus permissif (cf. partie D).
    detail = []
    for affirmation in affirmations:
        verdict = juge.invoke(f"""PASSAGES :
{contexte}

AFFIRMATION : {affirmation}

Cette affirmation peut-elle etre DEDUITE des passages ?
Une affirmation VRAIE mais absente des passages ne peut pas
en etre deduite : elle est ABSENTE.
Reponds par un seul mot : ETAYEE, PARTIELLE ou ABSENTE.""").content.strip().upper()

        # Une affirmation partiellement etayee compte pour moitie :
        # la binariser serait trop severe ou trop indulgent.
        poids = {"ETAYEE": 1.0, "PARTIELLE": 0.5}.get(
            verdict.split()[0] if verdict else "", 0.0)

        detail.append({"affirmation": affirmation,
                       "verdict": verdict, "poids": poids})

    return {
        "score": sum(d["poids"] for d in detail) / len(detail),
        "detail": detail,              # a CONSERVER pour l'audit
        "total": len(detail),
    }
