from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI


def construire_multi_query(base_vectorielle, k: int = 4):
    """Genere des variantes de chaque question et fusionne.

    Cout reel par question :
      - 1 appel de modele pour produire les variantes
      - N recherches vectorielles au lieu d'une
    Avec 3 variantes et k=4, on interroge 12 fois l'index et
    l'on obtient environ 7 documents uniques apres fusion.
    """
    return MultiQueryRetriever.from_llm(
        retriever=base_vectorielle.as_retriever(search_kwargs={"k": k}),
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3),
    )
