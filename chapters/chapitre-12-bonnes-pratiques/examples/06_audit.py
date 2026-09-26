"""Auto-audit statique des anti-patterns RAG vérifiables sans modèle."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severite(Enum):
    CRITIQUE = "critique"
    AVERTISSEMENT = "avertissement"


@dataclass(frozen=True)
class Constat:
    code: str
    severite: Severite
    message: str

    @property
    def critique(self) -> bool:
        return self.severite is Severite.CRITIQUE


def auditer_configuration(config: dict[str, object]) -> list[Constat]:
    findings: list[Constat] = []

    def add(code: str, critical: bool, message: str) -> None:
        severity = Severite.CRITIQUE if critical else Severite.AVERTISSEMENT
        findings.append(Constat(code, severity, message))

    if float(config.get("temperature", 0)) > 0:
        add("temperature", True, "La température doit être nulle pour un usage factuel.")

    ingestion = config.get("modele_embedding_ingestion")
    query = config.get("modele_embedding_requete")
    if not ingestion or not query:
        add("embedding_manquant", True, "Les deux modèles d'embedding doivent être déclarés.")
    elif ingestion != query:
        add("embedding_incompatible", True, "Ingestion et requête utilisent des embeddings différents.")

    checks = (
        ("prompt_contient_clause_refus", "clause_refus", True, "Clause de refus absente."),
        ("prompt_contient_clause_citation", "clause_citation", False, "Clause de citation absente."),
        ("journalise_scores_retrieval", "logs_scores", True, "Scores de retrieval non journalisés."),
        ("journalise_question_reformulee", "logs_reformulation", False, "Question reformulée non tracée."),
        ("filtrage_acces_au_retrieval", "acl", True, "Contrôle d'accès absent du retrieval."),
        ("golden_dataset_versionne", "golden_dataset", True, "Jeu de référence non versionné."),
    )
    for key, code, critical, message in checks:
        if not config.get(key):
            add(code, critical, message)

    k = int(config.get("k", 5))
    if k <= 0:
        add("k_invalide", True, "k doit être strictement positif.")
    elif k > 10:
        add("k_eleve", False, f"k={k} doit être justifié par un balayage mesuré.")
    return findings


if __name__ == "__main__":
    example = {
        "temperature": 0,
        "modele_embedding_ingestion": "même-modèle",
        "modele_embedding_requete": "même-modèle",
        "prompt_contient_clause_refus": True,
        "prompt_contient_clause_citation": True,
        "journalise_scores_retrieval": True,
        "journalise_question_reformulee": True,
        "filtrage_acces_au_retrieval": True,
        "golden_dataset_versionne": True,
        "k": 5,
    }
    print(auditer_configuration(example))
