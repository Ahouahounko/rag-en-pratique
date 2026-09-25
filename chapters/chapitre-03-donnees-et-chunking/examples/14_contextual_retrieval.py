GABARIT = """Voici un document complet :
<document>{document}</document>

Voici un extrait de ce document :
<extrait>{chunk}</extrait>

Redige en une a deux phrases le contexte necessaire pour situer
cet extrait dans le document (sujet, periode, entite concernee,
ce a quoi renvoient les references implicites).
Ne reponds que par ces phrases, sans preambule."""


def contextualiser(document: str, chunks: list[str], llm) -> list[str]:
    """
    Prefixe chaque chunk d'une description generee par un LLM.

    Point economique decisif : le document complet est identique
    d'un appel a l'autre. En le placant dans la partie mise en cache
    du prompt, on ne paie son traitement qu'une fois par document,
    et non une fois par chunk. Sans ce cache, la technique coute
    typiquement 10 a 50 fois plus cher.
    """
    enrichis = []
    for chunk in chunks:
        contexte = llm.generer(
            GABARIT.format(document=document, chunk=chunk),
            cache_prefixe=True,      # <-- la ligne qui rend cela viable
        )
        enrichis.append(f"{contexte.strip()}\n\n{chunk}")
    return enrichis
