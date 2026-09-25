# Exemples du chapitre 4

Ces fichiers proviennent des extraits du manuscrit et ont été complétés pour
devenir des exemples pédagogiques exécutables. OpenAI n'est utilisé que lorsque
l'extrait d'origine fait explicitement intervenir un LLM.

| # | Label LaTeX | Légende | Type | Fichier | Validation |
|---:|---|---|---|---|---|
| 01 | `lst:query_rewriting` | Query Rewriting --- reformulation contextuelle d'une requête | python | [`01_query_rewriting.py`](01_query_rewriting.py) | exécutable avec OpenAI |
| 02 | `lst:query_expansion` | Query Expansion et fusion par Reciprocal Rank Fusion | python | [`02_query_expansion.py`](02_query_expansion.py) | exécutable ; OpenAI facultatif |
| 03 | `lst:hyde` | HyDE --- recherche par document hypothétique | python | [`03_hyde.py`](03_hyde.py) | exécutable avec OpenAI |
| 04 | `lst:hybrid_search` | Hybrid Search --- dense et BM25 fusionnés par RRF | python | [`04_hybrid_search.py`](04_hybrid_search.py) | exécutable localement |
| 05 | `lst:reranking` | Re-ranking par cross-encoder --- la cascade en trois étapes | python | [`05_reranking.py`](05_reranking.py) | exécutable avec Hugging Face |
| 06 | `lst:mmr_pseudocode` | L'algorithme MMR, traduit en Python | python | [`06_mmr_pseudocode.py`](06_mmr_pseudocode.py) | exécutable |
| 07 | `lst:mmr` | MMR --- sélection diversifiée via le vector store | python | [`07_mmr.py`](07_mmr.py) | exécutable localement |
| 08 | `lst:reorder` | Réorganisation en V --- les meilleurs aux extrémités | python | [`08_reorder.py`](08_reorder.py) | exécutable localement |
| 09 | `lst:compression` | Compression contextuelle par extraction | python | [`09_compression.py`](09_compression.py) | exécutable avec OpenAI |
| 10 | `lst:pipeline_ordre` | La séquence complète du retrieval | python | [`10_pipeline_ordre.py`](10_pipeline_ordre.py) | exécutable |

## Convention d'exécution

- **localement** : aucune clé API n'est nécessaire ;
- **avec OpenAI** : `OPENAI_API_KEY` et `OPENAI_MODEL` sont nécessaires ;
- **avec Hugging Face** : le modèle public est téléchargé au premier lancement.
