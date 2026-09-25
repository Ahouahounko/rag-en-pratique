# tests/test_evaluation.py
import json
from pathlib import Path

import pytest
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy, context_precision, context_recall, faithfulness,
)

from src.generation.generator import Generateur
from src.retrieval.retriever import RetrieverHybride

JEU = Path("eval/jeu_reference.json")

# Seuils = ligne de base mesuree, PAS des objectifs ambitieux.
# On bloque une REGRESSION, on ne fixe pas une cible.
SEUILS = {
    "faithfulness": 0.75,
    "answer_relevancy": 0.70,
    "context_precision": 0.60,
    "context_recall": 0.65,
}


@pytest.fixture(scope="module")
def systeme():
    return RetrieverHybride(), Generateur()


def test_pas_de_regression(systeme):
    """Execute le jeu de reference et compare aux seuils.

    Ce test est LENT (plusieurs minutes) et coute des appels de
    modele : on le marque pour ne le lancer qu'a la demande et
    sur la branche principale, pas a chaque commit.
    """
    retriever, generateur = systeme
    cas = json.loads(JEU.read_text(encoding="utf-8"))

    donnees = {"question": [], "answer": [],
               "contexts": [], "ground_truth": []}

    for entree in cas:
        passages = retriever.chercher(entree["question"])
        reponse = generateur.repondre(entree["question"], passages)

        donnees["question"].append(entree["question"])
        donnees["answer"].append(reponse.texte)
        donnees["contexts"].append([p.texte for p in passages])
        donnees["ground_truth"].append(entree["reponse_attendue"])

    resultats = evaluate(
        dataset=Dataset.from_dict(donnees),
        metrics=[faithfulness, answer_relevancy,
                 context_precision, context_recall],
    )

    print("\n=== Evaluation ===")
    for nom, seuil in SEUILS.items():
        print(f"{nom:20s} : {resultats[nom]:.3f} (seuil {seuil})")

    # On verifie TOUTES les metriques avant d'echouer : sinon on
    # ne voit que la premiere qui casse, et l'on corrige a l'aveugle.
    echecs = [f"{nom} = {resultats[nom]:.3f} < {seuil}"
              for nom, seuil in SEUILS.items()
              if resultats[nom] < seuil]

    assert not echecs, "Regression detectee :\n" + "\n".join(echecs)


def test_abstention_sur_hors_sujet(systeme):
    """Le systeme refuse-t-il quand la reponse n'existe pas ?

    Test rapide et sans appel couteux au juge : il verifie
    seulement la presence de la formule d'abstention. A lancer
    a chaque commit.
    """
    retriever, generateur = systeme
    question = "Quel est le prix du billet pour Mars ?"

    passages = retriever.chercher(question)
    reponse = generateur.repondre(question, passages)

    assert "ne figure pas dans les documents" in reponse.texte.lower()
