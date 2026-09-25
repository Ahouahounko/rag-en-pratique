def verifier_ancrage(reponse: str, contexte: str, modele) -> dict:
    """Confronte chaque affirmation aux extraits fournis.

    Le verificateur ne voit PAS la question : il ne juge pas si
    la reponse est pertinente, seulement si elle est etayee.
    Cette separation evite la complaisance.
    """
    verdict = modele.invoke(f"""EXTRAITS DE REFERENCE :
{contexte}

TEXTE A VERIFIER :
{reponse}

Pour chaque affirmation du texte, indique une ligne au format :
AFFIRMATION | ETAYEE | PARTIELLE | ABSENTE

Ne juge pas la qualite du texte. Verifie uniquement si les
extraits contiennent bien ce qui est affirme.

Termine par une ligne : VERDICT: FIABLE ou VERDICT: A REVOIR
""").content

    return {
        "detail": verdict,
        "fiable": "VERDICT: FIABLE" in verdict,
    }
