from enum import Enum
from langchain_openai import ChatOpenAI


class Decision(Enum):
    CHERCHER = "chercher"
    REPONDRE = "repondre"
    CLARIFIER = "clarifier"


AIGUILLEUR = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def decider(question: str) -> Decision:
    """Faut-il consulter le corpus pour cette question ?

    En cas de doute, on cherche. Une recherche inutile coute
    quelques centaines de millisecondes ; une reponse donnee de
    memoire alors que le corpus contenait la verite officielle
    est une erreur bien plus grave.
    """
    verdict = AIGUILLEUR.invoke(f"""
Question : {question}

- "chercher"  : porte sur des donnees internes, recentes,
                chiffrees ou propres a l'organisation
- "repondre"  : culture generale, definition, concept stable
- "clarifier" : trop ambigue pour etre traitee telle quelle

Reponds par un seul mot :""").content.strip().lower()

    try:
        return Decision(verdict)
    except ValueError:
        return Decision.CHERCHER          # repli prudent
