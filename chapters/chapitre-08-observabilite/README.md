# Chapitre 8 — Observabilité du RAG

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/blob/main/chapters/chapitre-08-observabilite/08_observabilite.ipynb)

Ce chapitre couvre la création des jeux de référence, la calibration des juges,
l'attribution des erreurs, la latence et la détection de dérive.

## Contenu

- [`08_observabilite.ipynb`](08_observabilite.ipynb) : parcours pédagogique Colab ;
- [`examples/`](examples/) : 10 scripts autonomes ;
- [`runnable/`](runnable/) : démonstrations locales sans appel OpenAI.

## Ressources utiles

- [OpenAI Docs — observabilité et usage](https://developers.openai.com/api/docs/guides/agents-api/observability)
- [OpenAI Docs — tracing](https://developers.openai.com/api/docs/guides/agents-api/tracing)
- [RAGAS — métriques](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- [SciPy — test de Kolmogorov-Smirnov](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html)

Les exemples utilisant un juge OpenAI acceptent un client injecté. Les mesures
de latence, d'attribution et de dérive restent entièrement locales.
