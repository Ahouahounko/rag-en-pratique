"""Détecter les régressions d'une nouvelle version de prompt."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CasRegression:
    nom: str
    question: str
    extraits: list[str]
    doit_contenir: list[str] = field(default_factory=list)
    ne_doit_pas_contenir: list[str] = field(default_factory=list)
    doit_citer: list[str] = field(default_factory=list)


JEU_DE_TEST = [
    CasRegression(
        "cas nominal",
        "Quelle est la durée de la garantie ?",
        ["La garantie couvre 24 mois."],
        doit_contenir=["24 mois"],
        doit_citer=["doc_1"],
    ),
    CasRegression(
        "refus attendu",
        "La garantie est-elle transférable ?",
        ["La garantie couvre 24 mois."],
        doit_contenir=["ne permettent pas de répondre"],
        ne_doit_pas_contenir=["généralement", "en principe"],
    ),
]


def evaluer_version(
    generer_reponse: Callable[[list[str], str], str],
    cas: list[CasRegression] | None = None,
) -> list[dict[str, object]]:
    resultats = []
    for test in cas or JEU_DE_TEST:
        reponse = generer_reponse(test.extraits, test.question)
        texte = reponse.lower()
        erreurs = [
            *[f"absent: {mot}" for mot in test.doit_contenir if mot.lower() not in texte],
            *[f"interdit: {mot}" for mot in test.ne_doit_pas_contenir if mot.lower() in texte],
            *[f"citation absente: {source}" for source in test.doit_citer if source not in reponse],
        ]
        resultats.append(
            {"cas": test.nom, "succes": not erreurs, "erreurs": erreurs, "reponse": reponse}
        )
    return resultats


if __name__ == "__main__":
    def generateur_demo(extraits: list[str], question: str) -> str:
        if "transférable" in question:
            return "Les documents fournis ne permettent pas de répondre à cette question."
        return f"La garantie couvre 24 mois [doc_1]. Source : {extraits[0]}"

    print(evaluer_version(generateur_demo))
