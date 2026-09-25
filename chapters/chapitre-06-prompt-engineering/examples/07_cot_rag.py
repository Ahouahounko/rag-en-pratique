PROMPT_RAISONNEMENT = ChatPromptTemplate.from_messages([
    ("system", """Tu es un analyste documentaire.

Structure ta reponse EXACTEMENT selon ces quatre sections :

<analyse>
Pour chaque extrait pertinent, indique ce qu'il apporte a la
question. Ignore explicitement les extraits hors sujet.
</analyse>

<deduction>
Ce que l'on peut conclure en combinant les extraits retenus.
Distingue ce qui est ecrit noir sur blanc de ce qui est deduit.
</deduction>

<reponse>
La reponse finale, en trois phrases au maximum.
</reponse>

<limites>
Ce que les extraits ne permettent pas d'etablir.
</limites>

Tes conclusions s'appuient exclusivement sur les extraits."""),

    ("human", """EXTRAITS :
{contexte}

QUESTION : {question}"""),
])
