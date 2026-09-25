# Deux exemples suffisent, a condition de choisir le BON couple :
# un cas nominal et un cas de refus. C'est ce contraste qui
# enseigne la frontiere entre les deux comportements.
PROMPT_AVEC_EXEMPLES = ChatPromptTemplate.from_messages([
    ("system", SYSTEME),

    # --- Demonstration 1 : information presente ---
    ("human", """EXTRAITS :
[doc_1] cgv.pdf, page 8
La garantie couvre 24 mois a compter de la date d'achat.

QUESTION : Quelle est la duree de la garantie ?"""),
    ("ai", "La garantie couvre 24 mois a compter de la date "
           "d'achat [doc_1].\n\nSources : doc_1"),

    # --- Demonstration 2 : information absente ---
    ("human", """EXTRAITS :
[doc_1] cgv.pdf, page 8
La garantie couvre 24 mois a compter de la date d'achat.

QUESTION : La garantie est-elle transferable a un tiers ?"""),
    ("ai", "Les documents fournis ne permettent pas de repondre "
           "a cette question. L'extrait disponible precise la "
           "duree de la garantie [doc_1] mais n'aborde pas sa "
           "transmission."),

    # --- Cas reel ---
    ("human", """EXTRAITS :
{contexte}

QUESTION : {question}"""),
])
