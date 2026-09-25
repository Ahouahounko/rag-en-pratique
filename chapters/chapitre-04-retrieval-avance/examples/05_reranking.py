from sentence_transformers import CrossEncoder

# Modele leger et solide, ~80 Mo, tourne sans GPU.
# Il renvoie un score de pertinence pour une paire (question, texte).
RERANKER = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rechercher_et_reclasser(question: str, retriever,
                            n_candidats: int = 20,
                            n_final: int = 5) -> list:
    """Cascade : filtrage rapide, puis classement precis."""

    # Etape 1 - le filet large (quelques millisecondes)
    candidats = retriever.invoke(question)[:n_candidats]
    if not candidats:
        return []

    # Etape 2 - le jury (quelques dizaines de millisecondes)
    # Chaque paire est evaluee en tenant compte des interactions
    # directes entre les mots de la question et ceux du texte.
    paires = [(question, doc.page_content) for doc in candidats]
    scores = RERANKER.predict(paires)

    # Etape 3 - le classement final
    classes = sorted(zip(candidats, scores),
                     key=lambda couple: couple[1], reverse=True)

    return [doc for doc, _ in classes[:n_final]]
