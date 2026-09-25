"""Formater un contexte RAG compact, lisible et traçable."""

from rag_en_pratique.prompting import Passage, formater_simple

if __name__ == "__main__":
    passages = [
        Passage("La garantie couvre 24 mois.", {"source": "cgv.pdf", "page": 8}),
        Passage("Le retour est possible sous 30 jours.", {"source": "retours.md", "page": 1}),
    ]
    print(formater_simple(passages))
