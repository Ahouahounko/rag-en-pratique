# Chapitre 7 — Évaluation du RAG

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/blob/main/chapters/chapitre-07-evaluation/07_evaluation.ipynb)

Ce chapitre transforme les objectifs d'un système RAG en mesures reproductibles
du retrieval, de la fidélité et de la qualité globale.

## Contenu

- [`07_evaluation.ipynb`](07_evaluation.ipynb) : parcours pédagogique Colab ;
- [`examples/`](examples/) : quatre scripts autonomes ;
- [`runnable/`](runnable/) : exécution locale sans appel distant.

## Ressources utiles

- [OpenAI Docs — bonnes pratiques d'évaluation](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [OpenAI Developers — ressources sur les évaluations](https://developers.openai.com/learn/evals)
- [scikit-learn — nDCG](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html)
- [RAGAS — métriques](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)

Les métriques de rang sont entièrement locales. OpenAI intervient uniquement
comme juge facultatif pour les critères sémantiques.
