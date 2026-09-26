# Chapitre 12 — Bonnes pratiques

Pratiques d'ingénierie, d'expérimentation et d'exploitation qui rendent un RAG
mesurable, explicable et durable.

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/blob/main/chapters/chapitre-12-bonnes-pratiques/12_bonnes_pratiques.ipynb)

## Parcours exécutable

- [`12_bonnes_pratiques.ipynb`](12_bonnes_pratiques.ipynb) : six expériences guidées ;
- [`examples`](examples/) : scripts réutilisables et injectables ;
- [`runnable/run_chapter.py`](runnable/run_chapter.py) : démonstrations locales sans appel distant.

## Principes du chapitre

- nettoyer avant le chunking ;
- mesurer le chunking sur des questions réelles ;
- choisir `k` à partir du rappel mesuré ;
- versionner le prompt et le jeu de référence ;
- journaliser scores et latences en minimisant les données personnelles ;
- automatiser les vérifications statiques ;
- modifier une seule variable à la fois et prévoir le retour arrière.

## Ressources officielles

- [OpenAI Docs — production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)
- [OpenAI Docs — evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI Docs — rate limits](https://developers.openai.com/api/docs/guides/rate-limits)

## Code du manuscrit

Ce chapitre contient **6 blocs de code** issus du manuscrit. Consultez
[l'inventaire des exemples](examples/README.md).
