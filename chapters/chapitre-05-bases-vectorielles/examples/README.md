# Exemples du chapitre 5

Les fichiers de ce dossier sont extraits automatiquement du manuscrit. 
Le contenu est conservé tel quel afin de permettre sa revue avant transformation 
en exemple autonome ou en notebook exécutable.

| # | Label LaTeX | Légende | Type | Fichier | Validation |
|---:|---|---|---|---|---|
| 01 | `lst:faiss_hnsw` | FAISS --- construction et interrogation d'un index HNSW | python | [`01_faiss_hnsw.py`](01_faiss_hnsw.py) | syntaxe validée |
| 02 | `lst:faiss_ivf` | FAISS --- index IVF pour les très grands corpus | python | [`02_faiss_ivf.py`](02_faiss_ivf.py) | syntaxe validée |
| 03 | `lst:filtrage_metadonnees` | Recherche vectorielle avec filtres de métadonnées | python | [`03_filtrage_metadonnees.py`](03_filtrage_metadonnees.py) | syntaxe validée |
| 04 | `lst:chroma` | Chroma --- indexation et recherche filtrée | python | [`04_chroma.py`](04_chroma.py) | syntaxe validée |
| 05 | `lst:qdrant` | Qdrant --- collection configurée pour la production | python | [`05_qdrant.py`](05_qdrant.py) | syntaxe validée |
| 06 | `lst:pinecone` | Pinecone --- index serverless et insertion | python | [`06_pinecone.py`](06_pinecone.py) | syntaxe validée |
| 07 | `lst:self_query` | Self-Query --- description du schéma et construction | python | [`07_self_query.py`](07_self_query.py) | syntaxe validée |
| 08 | `lst:multi_query` | Multi-Query Retriever --- variantes et fusion intégrées | python | [`08_multi_query.py`](08_multi_query.py) | syntaxe validée |
| 09 | `lst:ensemble` | Ensemble Retriever — BM25 + dense avec pondération configurable | python | [`09_ensemble.py`](09_ensemble.py) | syntaxe validée |
| 10 | `lst:text_to_sql` | Text-to-SQL --- chaîne complète et périmètre restreint | python | [`10_text_to_sql.py`](10_text_to_sql.py) | syntaxe validée |
| 11 | `lst:router_rag` | Routage --- orientation vers la source pertinente | python | [`11_router_rag.py`](11_router_rag.py) | syntaxe validée |
| 12 | `lst:chapitre5_12` | Exemple sans légende | text | [`12_chapitre5_12.txt`](12_chapitre5_12.txt) | à valider |
| 13 | `lst:rag_iteratif` | RAG itératif --- raisonnement en plusieurs sauts | python | [`13_rag_iteratif.py`](13_rag_iteratif.py) | syntaxe validée |
| 14 | `lst:rag_adaptatif` | RAG adaptatif chercher seulement si nécessaire | python | [`14_rag_adaptatif.py`](14_rag_adaptatif.py) | syntaxe validée |

## Convention de validation

- **syntaxe validée** : le fichier Python passe l'analyse syntaxique ;
- **extrait pédagogique** : le bloc est partiel, contient des ellipses ou demande un contexte ;
- **à valider** : commande, configuration, prompt ou autre contenu à tester manuellement.
