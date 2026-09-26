"""Effacement coordonné du cache, de l'index, du registre et des journaux."""

from __future__ import annotations

import hashlib
import logging
from dataclasses import asdict, dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BilanEffacement:
    documents: int
    passages: int
    entrees_cache: int
    journaux_anonymises: bool
    simulation: bool = False


def _reference_audit(identifiant: str) -> str:
    return hashlib.sha256(identifiant.encode("utf-8")).hexdigest()[:12]


def effacer_personne(
    identifiant: str,
    registre,
    index,
    cache,
    journaux,
    *,
    simulation: bool = False,
) -> dict[str, object]:
    if not identifiant.strip():
        raise ValueError("identifiant ne peut pas être vide")

    documents = list(registre.documents_mentionnant(identifiant))
    passage_ids = [
        passage_id
        for document in documents
        for passage_id in registre.passages_de(document)
    ]
    if simulation:
        return asdict(
            BilanEffacement(len(documents), len(passage_ids), 0, False, simulation=True)
        )

    cache_count = cache.purger_si_source_dans(documents)
    if passage_ids:
        index.supprimer(passage_ids)
    registre.oublier(documents)
    journaux.anonymiser_occurrences(identifiant)

    report = BilanEffacement(len(documents), len(passage_ids), cache_count, True)
    logger.info("Effacement terminé | référence=%s | bilan=%s", _reference_audit(identifiant), report)
    return asdict(report)


if __name__ == "__main__":
    print("Exemple prêt : injectez le registre, l'index, le cache et les journaux.")
