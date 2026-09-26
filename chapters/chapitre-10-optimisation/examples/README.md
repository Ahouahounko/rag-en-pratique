# Exemples du chapitre 10

Chaque script expose une fonction ou une classe injectable afin de pouvoir être
testé sans réseau, tout en utilisant le vrai fournisseur lorsque vous l'activez.

| # | Sujet | Fichier | Exécution |
|---:|---|---|---|
| 01 | Streaming SSE | [`01_streaming.py`](01_streaming.py) | OpenAI Responses API avec client injectable |
| 02 | Cache sémantique | [`02_cache_semantique.py`](02_cache_semantique.py) | Local, encodeur injectable |
| 03 | Token pruning | [`03_token_pruning.py`](03_token_pruning.py) | Hugging Face facultatif, scorer injectable |
| 04 | Résumé des chunks | [`04_summarize_chunks.py`](04_summarize_chunks.py) | OpenAI facultatif, résumeur injectable |
| 05 | Routage économique | [`05_routeur_economique.py`](05_routeur_economique.py) | Heuristiques locales puis OpenAI |
| 06 | Batch embedding | [`06_batch_embedding.py`](06_batch_embedding.py) | Local ou fournisseur choisi, avec retry |

## Principes pédagogiques

- mesurer avant d'optimiser ;
- ne résumer que les chunks réellement trop longs ;
- router d'abord avec des heuristiques gratuites ;
- ne réessayer que les erreurs temporaires connues en production ;
- conserver l'ordre des embeddings lors du traitement par lots ;
- tester les optimisations contre les seuils de qualité du chapitre 7.

Le runner local est disponible dans [`../runnable`](../runnable/). Le notebook
[`../10_optimisation.ipynb`](../10_optimisation.ipynb) reprend les six exemples
avec les cellules de configuration OpenAI et Hugging Face.
