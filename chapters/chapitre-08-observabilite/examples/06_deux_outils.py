# --- Approche "campagne de mesure" (style RAGAS) -------------
# On evalue un jeu entier et on obtient des scores continus,
# a lire ensemble comme au tableau des configurations.

resultats = evaluer(
    jeu=jeu_de_reference,
    metriques=[fidelite, pertinence_reponse,
               pertinence_contexte, rappel_contexte],
    modele_juge=JUGE,            # a CONSIGNER avec les resultats
)
print(resultats.moyennes())
# {"fidelite": 0.82, "pertinence_reponse": 0.79, ...}


# --- Approche "test de non-regression" (style DeepEval) ------
# Chaque cas devient une assertion. Le test ECHOUE sous le seuil,
# et l'integration continue bloque le deploiement.

def test_pas_de_regression_fidelite():
    cas = CasDeTest(
        question="Quelle est la duree de la garantie ?",
        reponse=systeme.repondre(question),
        contexte=systeme.dernier_contexte(),
    )
    metrique = Fidelite(seuil=0.80, modele_juge=JUGE)

    assert metrique.mesurer(cas) >= metrique.seuil, (
        f"Fidelite tombee a {metrique.score:.2f}. "
        f"Justification du juge : {metrique.raison}"
    )
