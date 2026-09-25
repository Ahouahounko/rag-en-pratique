def rag_step_back(question: str, retriever, modele) -> str:
    """Cherche la regle generale avant de traiter le cas precis."""

    # --- 1. Formuler la question de recul ---
    generale = modele.invoke(f"""
Formule la question generale dont la reponse permettrait de
trancher le cas particulier ci-dessous. Vise la regle, la
politique ou le principe applicable, pas le cas lui-meme.

Cas particulier : {question}

Question generale :""").content.strip()

    # --- 2. Chercher pour les DEUX questions ---
    # La question specifique ramene les documents proches du cas ;
    # la generale ramene la regle. On a besoin des deux.
    specifiques = retriever.invoke(question)
    generaux = retriever.invoke(generale)

    vus = {p.page_content for p in specifiques}
    tous = specifiques + [p for p in generaux
                          if p.page_content not in vus]

    # --- 3. Repondre en explicitant la regle mobilisee ---
    contexte = formater_simple(tous)

    return modele.invoke(f"""EXTRAITS :
{contexte}

Principe general recherche : {generale}
Question posee : {question}

Reponds a la question posee. Enonce d'abord la regle generale
applicable, puis son application au cas. Cite tes sources.
""").content
