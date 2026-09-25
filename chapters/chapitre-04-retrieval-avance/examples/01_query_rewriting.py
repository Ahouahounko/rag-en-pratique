from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Un modele leger suffit : la tache est mecanique, pas cognitive.
# temperature=0 -> la meme question donne toujours la meme
# reformulation, ce qui rend le systeme reproductible et debogable.
REWRITER = ChatOpenAI(model="gpt-4o-mini", temperature=0)

PROMPT_REECRITURE = ChatPromptTemplate.from_template("""
Tu reformules des questions pour un moteur de recherche documentaire.

Regles :
- Remplace les pronoms et les references implicites par ce qu'ils
  designent, en t'appuyant sur l'historique fourni.
- Rends la question comprehensible sans aucun contexte exterieur.
- Emploie le vocabulaire du domaine plutot que le registre familier.
- Conserve l'intention exacte. Ne reponds PAS a la question.

{historique}
Question originale : {question}

Question reformulee :""")


def reecrire_requete(question: str, historique: list[str] = None) -> str:
    """Rend une question autonome et cherchable.

    historique : les derniers echanges de la conversation.
                 Trois suffisent : au-dela, on paye des tokens
                 pour du contexte que le modele n'utilisera pas.
    """
    bloc_historique = ""
    if historique:
        derniers = historique[-3:]
        bloc_historique = ("Historique de la conversation :\n"
                           + "\n".join(f"- {tour}" for tour in derniers)
                           + "\n\n")

    chaine = PROMPT_REECRITURE | REWRITER
    reformulee = chaine.invoke({
        "question": question,
        "historique": bloc_historique,
    }).content.strip()

    return reformulee


# Exemple
historique = ["L'utilisateur consulte les conditions de vente en ligne."]
print(reecrire_requete("Et pour les delais ?", historique))
# -> "Quels sont les delais de livraison des commandes en ligne ?"
