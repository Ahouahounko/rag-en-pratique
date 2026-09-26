"""Journalisation structurée avec minimisation des données par défaut."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import time
import uuid
from collections.abc import Callable

logger = logging.getLogger("rag")


def pseudonymiser(value: str, secret: str) -> str:
    if not secret:
        raise ValueError("Une clé HMAC de journalisation est obligatoire")
    return hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()[:20]


def empreinte_contenu(value: str) -> dict[str, object]:
    return {
        "sha256": hashlib.sha256(value.encode()).hexdigest()[:20],
        "longueur": len(value),
    }


def repondre_et_journaliser(
    question: str,
    utilisateur: str,
    retriever,
    generateur,
    *,
    reformuler: Callable[[str], str] = lambda value: value,
    secret: str | None = None,
    journaliser_contenu: bool = False,
    horloge: Callable[[], float] = time.perf_counter,
    trace_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
) -> dict[str, object]:
    log_secret = secret or os.getenv("RAG_LOG_HMAC_KEY", "")
    trace = trace_factory()
    started = horloge()
    used_question = reformuler(question)
    reformulated_at = horloge()
    passages = retriever.chercher(used_question)
    retrieved_at = horloge()
    response = generateur.repondre(used_question, passages)
    finished_at = horloge()

    journal: dict[str, object] = {
        "trace": trace,
        "utilisateur": pseudonymiser(utilisateur, log_secret),
        "question": question if journaliser_contenu else empreinte_contenu(question),
        "question_utilisee": (
            used_question if journaliser_contenu else empreinte_contenu(used_question)
        ),
        "passages": [
            {
                "source": (
                    passage.source
                    if journaliser_contenu
                    else pseudonymiser(str(passage.source), log_secret)
                ),
                "page": passage.page,
                "score": round(passage.score_rerank or passage.score_dense, 3),
            }
            for passage in passages
        ],
        "reponse": response.texte if journaliser_contenu else empreinte_contenu(response.texte),
        "confiance": response.confiance,
        "version_prompt": response.version_prompt,
        "latences_ms": {
            "reformulation": round((reformulated_at - started) * 1_000),
            "retrieval": round((retrieved_at - reformulated_at) * 1_000),
            "generation": round((finished_at - retrieved_at) * 1_000),
            "total": round((finished_at - started) * 1_000),
        },
        "tokens": getattr(response, "tokens", None),
    }
    logger.info(json.dumps(journal, ensure_ascii=False))
    return {"reponse": response, "trace": trace, "journal": journal}


if __name__ == "__main__":
    print("Exemple prêt : configurez RAG_LOG_HMAC_KEY et injectez retriever/générateur.")
