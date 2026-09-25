"""Explorer systématiquement taille, overlap et stratégie de chunking."""

import itertools
import re

TAILLES = [12, 20]
OVERLAPS = [0.0, 0.20]
STRATEGIES = ["fixe", "paragraphes"]


def decouper(document: str, taille: int, overlap: int, strategie: str) -> list[str]:
    if strategie == "paragraphes":
        return [partie.strip() for partie in document.split("\n\n") if partie.strip()]
    mots = document.split()
    pas = max(1, taille - overlap)
    return [" ".join(mots[index : index + taille]) for index in range(0, len(mots), pas)]


def score_lexical(question: str, chunk: str) -> int:
    mots_question = set(re.findall(r"\w+", question.lower()))
    mots_chunk = set(re.findall(r"\w+", chunk.lower()))
    return len(mots_question & mots_chunk)


def evaluer(questions: list[tuple[str, str]], chunks: list[str]) -> dict[str, float]:
    succes = 0
    for question, terme_attendu in questions:
        meilleur = max(chunks, key=lambda chunk: score_lexical(question, chunk))
        succes += terme_attendu.lower() in meilleur.lower()
    return {"precision_contextuelle": succes / len(questions)}


def explorer(corpus: list[str], questions: list[tuple[str, str]]) -> list[dict[str, object]]:
    resultats: list[dict[str, object]] = []
    for taille, ratio, strategie in itertools.product(TAILLES, OVERLAPS, STRATEGIES):
        chunks = [
            chunk
            for document in corpus
            for chunk in decouper(document, taille, int(taille * ratio), strategie)
        ]
        resultats.append(
            {
                "taille": taille,
                "overlap": ratio,
                "strategie": strategie,
                "nombre_chunks": len(chunks),
                **evaluer(questions, chunks),
            }
        )
    return resultats


if __name__ == "__main__":
    corpus = [
        "Retours\n\nLes produits sont retournables pendant trente jours avec un reçu.",
        "Livraison\n\nLa livraison standard prend cinq jours ouvrés avec suivi.",
    ]
    questions = [("Quel délai pour un retour ?", "trente"), ("Délai livraison ?", "cinq")]
    resultats = explorer(corpus, questions)
    for resultat in resultats:
        print(resultat)
    print("Meilleure configuration :", max(resultats, key=lambda r: r["precision_contextuelle"]))
