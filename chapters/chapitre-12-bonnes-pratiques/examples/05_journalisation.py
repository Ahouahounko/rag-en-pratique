import json
import logging
import time
import uuid

logger = logging.getLogger("rag")


def repondre_et_journaliser(question: str, utilisateur: str,
                            retriever, generateur) -> dict:
    """Pipeline instrumente de bout en bout.

    On journalise en JSON plutot qu'en texte libre : les champs
    deviennent requetables, ce qui permet de repondre a des
    questions du type "toutes les requetes ou le meilleur score
    etait sous 0.4 la semaine derniere".
    """
    trace = str(uuid.uuid4())       # relie toutes les etapes
    depart = time.perf_counter()

    question_utilisee = reformuler(question)
    t_reformulation = time.perf_counter()

    passages = retriever.chercher(question_utilisee)
    t_retrieval = time.perf_counter()

    reponse = generateur.repondre(question_utilisee, passages)
    fin = time.perf_counter()

    journal = {
        "trace": trace,
        "utilisateur": pseudonymiser(utilisateur),   # jamais en clair

        # La question ORIGINALE et la reformulee : quand une
        # reponse part de travers, c'est presque toujours la
        # reformulation qu'il faut regarder en premier.
        "question": question,
        "question_utilisee": question_utilisee,

        # Les passages AVEC leurs scores : sans les scores, on ne
        # peut pas distinguer "mauvais passages recuperes" de
        # "bons passages mal exploites".
        "passages": [
            {"source": p.source, "page": p.page,
             "score": round(p.score_rerank or p.score_dense, 3)}
            for p in passages
        ],

        "reponse": reponse.texte,
        "confiance": reponse.confiance,
        "version_prompt": reponse.version_prompt,

        "latences_ms": {
            "reformulation": int((t_reformulation - depart) * 1000),
            "retrieval": int((t_retrieval - t_reformulation) * 1000),
            "generation": int((fin - t_retrieval) * 1000),
            "total": int((fin - depart) * 1000),
        },
        "tokens": reponse.tokens,
    }

    logger.info(json.dumps(journal, ensure_ascii=False))
    return {"reponse": reponse, "trace": trace}
