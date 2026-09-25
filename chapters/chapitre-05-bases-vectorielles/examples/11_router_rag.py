from enum import Enum
from langchain_openai import ChatOpenAI


class Source(Enum):
    DOCUMENTS = "documents"
    TABLES = "tables"
    LES_DEUX = "les_deux"


CLASSIFIEUR = ChatOpenAI(model="gpt-4o-mini", temperature=0)

GABARIT = """Determine ou chercher la reponse a cette question.

- "documents" : procedures, politiques, explications, definitions
- "tables"    : chiffres, comptages, agregats, evolutions datees
- "les_deux"  : la reponse exige un chiffre ET son explication

Question : {question}

Reponds par un seul mot :"""


def router(question: str) -> Source:
    """Classe la question. En cas de doute, on privilegie les
    documents : une reponse documentaire imprecise se repere,
    un chiffre faux passe inapercu."""
    reponse = CLASSIFIEUR.invoke(
        GABARIT.format(question=question)
    ).content.strip().lower()

    try:
        return Source(reponse)
    except ValueError:
        return Source.DOCUMENTS          # repli prudent
