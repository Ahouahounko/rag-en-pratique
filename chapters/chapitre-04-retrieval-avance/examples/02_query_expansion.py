from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Temperature legerement positive : on VEUT de la variete ici,
# contrairement a la reformulation ou l'on cherchait la stabilite.
GENERATEUR = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

PROMPT_VARIANTES = ChatPromptTemplate.from_template("""
Genere {n} reformulations de la question ci-dessous, chacune sous un
angle different : synonymes metier, tournure plus generale, tournure
plus specifique.
Une reformulation par ligne, sans numerotation, sans commentaire.

Question : {question}
""")


def generer_variantes(question: str, n: int = 3) -> list[str]:
    """Produit n reformulations, plus la question d'origine."""
    reponse = (PROMPT_VARIANTES | GENERATEUR).invoke({
        "question": question, "n": n,
    }).content

    variantes = [ligne.strip() for ligne in reponse.split("\n")
                 if ligne.strip()]

    # La question originale reste dans le lot : la reformulation
    # peut deriver, l'originale sert de garde-fou.
    return [question] + variantes


def fusion_rrf(listes: list[list], k: int = 60) -> list:
    """Fusionne plusieurs listes de resultats par leurs RANGS.

    On ignore volontairement les scores de similarite : ils ne sont
    pas comparables d'une recherche a l'autre (cf. texte).
    """
    cumul = {}

    for resultats in listes:
        for rang, doc in enumerate(resultats, start=1):
            cle = doc.page_content[:120]        # identifiant du chunk

            if cle not in cumul:
                cumul[cle] = {"score": 0.0, "doc": doc}

            cumul[cle]["score"] += 1.0 / (k + rang)

    ordonne = sorted(cumul.values(),
                     key=lambda e: e["score"], reverse=True)
    return [e["doc"] for e in ordonne]


def recherche_elargie(question: str, retriever, n: int = 3, k: int = 5):
    """Cherche depuis plusieurs formulations, puis fusionne."""
    variantes = generer_variantes(question, n)
    listes = [retriever.invoke(v) for v in variantes]
    return fusion_rrf(listes)[:k]
