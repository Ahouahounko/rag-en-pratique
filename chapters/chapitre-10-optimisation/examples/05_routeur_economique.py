from enum import Enum

from langchain_openai import ChatOpenAI


class Complexite(Enum):
    SIMPLE = "simple"        # reponse directe, un seul passage
    MOYENNE = "moyenne"      # synthese de deux ou trois passages
    COMPLEXE = "complexe"    # raisonnement multi-documents, ou critique


MODELES = {
    Complexite.SIMPLE:   "gpt-4o-mini",
    Complexite.MOYENNE:  "gpt-4o-mini",
    Complexite.COMPLEXE: "gpt-4o",
}

# Sujets ou l'erreur coute cher : ils partent au modele principal
# quelle que soit la simplicite apparente de la question.
SUJETS_CRITIQUES = ("juridique", "medical", "contrat", "sanction",
                    "licenciement", "conformite")

MARQUEURS_SIMPLES = ("quel est", "combien", "quand", "qui est",
                     "quelle est la date", "quel montant")
MARQUEURS_COMPLEXES = ("compare", "implique", "synthese", "analyse",
                       "impact de", "difference entre", "pourquoi")


def classer(question: str, classifieur=None) -> Complexite:
    """Deux etages : heuristique gratuite, puis modele si besoin."""
    texte = question.lower()

    # --- Etage 1 : gratuit, tranche la majorite des cas ---
    if any(sujet in texte for sujet in SUJETS_CRITIQUES):
        return Complexite.COMPLEXE          # la criticite prime

    if any(m in texte for m in MARQUEURS_COMPLEXES):
        return Complexite.COMPLEXE

    if any(m in texte for m in MARQUEURS_SIMPLES) and len(texte.split()) < 15:
        return Complexite.SIMPLE

    # --- Etage 2 : on ne paie un appel que sur les cas ambigus ---
    if classifieur is None:
        return Complexite.MOYENNE           # repli prudent

    verdict = classifieur.invoke(f"""Classe cette question :
- "simple"   : reponse directe dans un seul passage
- "moyenne"  : synthese de deux ou trois passages
- "complexe" : raisonnement multi-documents, ou question critique

Question : {question}

Un seul mot :""").content.strip().lower()

    try:
        return Complexite(verdict)
    except ValueError:
        return Complexite.MOYENNE


def modele_pour(question: str, classifieur=None) -> ChatOpenAI:
    complexite = classer(question, classifieur)
    return ChatOpenAI(model=MODELES[complexite], temperature=0)
