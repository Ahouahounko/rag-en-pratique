PROMPT_FILTRAGE = """Tu evalues le realisme de questions destinees
a tester un moteur de recherche immobilier.

Voici des questions que nous avons notees manuellement :

REALISTES
- "Quelle est la taxe fonciere du 12 rue des Lilas ?"
  Note 5 - typique, concise, ciblee sur un bien.
- "Montre-moi les maisons 3 chambres a Bordeaux avec un jardin."
  Note 5 - recherche filtree naturelle.

IRREALISTES
- "De quelle couleur est la troisieme brique de la cheminee du
   bien vendu hier ?"
  Note 1 - specificite absurde, personne ne demande cela.
- "Quelle est la surface cumulee de tous les biens du 33000 ?"
  Note 2 - agregation etrange, hors des usages de recherche.

Note la question suivante de 1 a 5 et justifie brievement.

QUESTION : {question}

Explication : [breve]
Note : [1-5]"""


def filtrer(questions: list[dict], modele,
            note_minimale: int = 4) -> list[dict]:
    """Ecarte les questions peu realistes.

    L'echelle 1-5 est ici legitime alors que nous recommandons
    ailleurs des jugements binaires : on ne mesure pas une
    performance, on CLASSE des candidats pour couper la queue
    de distribution. La finesse de l'echelle sert le tri, elle
    n'a pas a etre reproductible au dixieme pres.
    """
    retenues = []
    for q in questions:
        sortie = modele.invoke(
            PROMPT_FILTRAGE.format(question=q["question"])).content
        note = extraire_note(sortie)
        if note >= note_minimale:
            retenues.append({**q, "note_realisme": note})
    return retenues
