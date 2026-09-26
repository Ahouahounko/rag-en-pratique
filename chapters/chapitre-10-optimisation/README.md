# Chapitre 10 — Optimisation

Optimiser un RAG sans sacrifier sa qualité : latence réelle et perçue, coûts,
contexte et passage à l'échelle.

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/blob/main/chapters/chapitre-10-optimisation/10_optimisation.ipynb)

## Parcours exécutable

- [`10_optimisation.ipynb`](10_optimisation.ipynb) : les six expériences guidées ;
- [`examples`](examples/) : scripts autonomes et injectables ;
- [`runnable/run_chapter.py`](runnable/run_chapter.py) : validation locale sans appel distant.

OpenAI intervient uniquement dans les exemples de streaming, de résumé et de
routage. Le token pruning peut charger un pipeline Hugging Face. Le cache et la
vectorisation par lots restent indépendants du fournisseur.

## Ressources

- [OpenAI Docs — Prompt Caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [OpenAI Docs — Batch API](https://developers.openai.com/api/docs/guides/batch)
- [OpenAI Docs — optimisation de la latence](https://developers.openai.com/api/docs/guides/latency-optimization)
- [Hugging Face — pipelines Transformers](https://huggingface.co/docs/transformers/main_classes/pipelines)

## Code du manuscrit

Ce chapitre contient **6 blocs de code** issus du manuscrit. Consultez
[l'inventaire des exemples](examples/README.md).
