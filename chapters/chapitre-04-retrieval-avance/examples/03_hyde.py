from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

REDACTEUR = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

# Le prompt impose le REGISTRE de vos documents reels.
# C'est le point critique : un hypothetique redige comme un
# article de blog ne se rapprochera pas d'une norme technique.
PROMPT_HYDE = ChatPromptTemplate.from_template("""
Redige un extrait de documentation technique de 3 a 5 phrases qui
repond a la question suivante.
Ecris au present, sur un ton factuel et impersonnel, comme un
manuel officiel. N'indique jamais qu'il s'agit d'une hypothese.

Question : {question}

Extrait :""")


def recherche_hyde(question: str, base_vectorielle,
                   modele_embedding, k: int = 5) -> list:
    """Cherche des documents reels proches d'une reponse inventee."""

    # 1. Rediger la reponse hypothetique
    hypothese = (PROMPT_HYDE | REDACTEUR).invoke(
        {"question": question}
    ).content

    # 2. Vectoriser CE TEXTE, et non la question
    vecteur = modele_embedding.embed_query(hypothese)

    # 3. Chercher les vrais documents voisins de ce vecteur
    return base_vectorielle.similarity_search_by_vector(vecteur, k=k)
