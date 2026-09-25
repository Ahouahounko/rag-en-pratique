def formater_simple(passages: list) -> str:
    """Assemble les passages avec un en-tete et un separateur.

    L'identifiant doc_N est GENERE ICI et devra etre conserve
    par l'application : c'est lui qui permettra de retrouver
    la source quand le modele la citera.
    """
    blocs = []

    for numero, passage in enumerate(passages, start=1):
        source = passage.metadata.get("source", "document inconnu")
        page = passage.metadata.get("page", "?")

        blocs.append(
            f"[doc_{numero}] {source}, page {page}\n"
            f"{passage.page_content}"
        )

    # Un separateur VISIBLE : sans lui, deux passages successifs
    # se lisent comme un texte continu.
    return "\n\n---\n\n".join(blocs)
