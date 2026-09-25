from langchain_openai import ChatOpenAI

MODELE = ChatOpenAI(model="gpt-4o", temperature=0)


def rag_iteratif(question: str, retriever,
                 max_iterations: int = 3) -> dict:
    """Cherche, evalue, recherche si necessaire.

    La borne max_iterations n'est pas decorative : sans elle,
    une question mal posee peut boucler indefiniment en
    consommant un appel de modele a chaque tour.
    """
    contexte, requete = [], question

    for tour in range(max_iterations):
        contexte.extend(retriever.invoke(requete))

        texte = "\n\n".join(d.page_content for d in contexte[:8])

        verdict = MODELE.invoke(f"""
Question initiale : {question}

Contexte accumule :
{texte[:3000]}

Ce contexte suffit-il a repondre COMPLETEMENT ?
- Si oui, reponds exactement : SUFFISANT
- Sinon, reponds : MANQUE: <la sous-question precise a chercher>
""").content.strip()

        if verdict.startswith("SUFFISANT"):
            break

        if verdict.startswith("MANQUE:"):
            requete = verdict.split(":", 1)[1].strip()
        else:
            break        # reponse inattendue : on arrete plutot que d'insister

    reponse = MODELE.invoke(f"""
Contexte : {texte[:4000]}
Question : {question}
Reponds uniquement a partir du contexte, en citant tes sources.
""").content

    return {"reponse": reponse, "tours": tour + 1, "sources": contexte}
