PROMPT_JUGE_FAITHFULNESS = """Tu es un evaluateur impartial.

CRITERE : faithfulness (fidelite au contexte). Une reponse est fidele si chaque affirmation
qu'elle contient peut etre retrouvee ou deduite sans ambiguite
depuis les PASSAGES fournis.

PASSAGES :
{contexte}

QUESTION : {question}

REPONSE A EVALUER :
{reponse}

PROCEDURE - suis-la dans l'ordre :
1. Enumere les affirmations distinctes de la reponse.
2. Pour chacune, cite le fragment de passage qui l'etaye, ou
   ecris "aucun" si tu n'en trouves pas.
3. Compte les affirmations etayees et le total.
4. Attribue la note.

ECHELLE :
1 = la majorite des affirmations sont inventees
2 = plus de la moitie ne sont pas etayees
3 = environ la moitie est etayee
4 = quasi-totalite etayee, une ou deux affirmations douteuses
5 = toutes les affirmations sont etayees

REGLES DE NEUTRALITE :
- La LONGUEUR de la reponse n'entre PAS dans ton evaluation.
- Le STYLE n'entre PAS dans ton evaluation.
- Une affirmation VRAIE mais absente des passages est NON ETAYEE.
  C'est le point le plus important : tu juges l'ancrage, pas la
  verite du monde.

RAISONNEMENT : [ton analyse, affirmation par affirmation]
NOTE : [1-5]"""
