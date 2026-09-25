# Exemples du chapitre 4

Les fichiers de ce dossier sont extraits automatiquement du manuscrit. 
Le contenu est conservé tel quel afin de permettre sa revue avant transformation 
en exemple autonome ou en notebook exécutable.

| # | Label LaTeX | Légende | Type | Fichier | Validation |
|---:|---|---|---|---|---|
| 01 | `lst:query_rewriting` | Query Rewriting --- reformulation contextuelle d'une requête | python | [`01_query_rewriting.py`](01_query_rewriting.py) | syntaxe validée |
| 02 | `lst:query_expansion` | Query Expansion et fusion par Reciprocal Rank Fusion | python | [`02_query_expansion.py`](02_query_expansion.py) | syntaxe validée |
| 03 | `lst:hyde` | HyDE --- recherche par document hypothétique | python | [`03_hyde.py`](03_hyde.py) | syntaxe validée |
| 04 | `lst:hybrid_search` | Hybrid Search --- dense et BM25 fusionnés par RRF | python | [`04_hybrid_search.py`](04_hybrid_search.py) | syntaxe validée |
| 05 | `lst:reranking` | Re-ranking par cross-encoder --- la cascade en trois étapes | python | [`05_reranking.py`](05_reranking.py) | syntaxe validée |
| 06 | `lst:mmr_pseudocode` | L'algorithme MMR, en pseudo-code | text | [`06_mmr_pseudocode.txt`](06_mmr_pseudocode.txt) | à valider |
| 07 | `lst:mmr` | MMR --- sélection diversifiée via le vector store | python | [`07_mmr.py`](07_mmr.py) | syntaxe validée |
| 08 | `lst:reorder` | Réorganisation en V --- les meilleurs aux extrémités | python | [`08_reorder.py`](08_reorder.py) | syntaxe validée |
| 09 | `lst:compression` | Compression contextuelle par extraction | python | [`09_compression.py`](09_compression.py) | syntaxe validée |
| 10 | `lst:pipeline_ordre` | La séquence complète du retrieval, en pseudo-code | text | [`10_pipeline_ordre.txt`](10_pipeline_ordre.txt) | à valider |

## Convention de validation

- **syntaxe validée** : le fichier Python passe l'analyse syntaxique ;
- **extrait pédagogique** : le bloc est partiel, contient des ellipses ou demande un contexte ;
- **à valider** : commande, configuration, prompt ou autre contenu à tester manuellement.
