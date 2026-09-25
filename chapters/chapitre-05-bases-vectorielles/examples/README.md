# Exemples du chapitre 5

Chaque fichier peut être lu séparément et expose des fonctions réutilisables.

| # | Sujet | Fichier | Exécution |
|---:|---|---|---|
| 01 | FAISS HNSW | [`01_faiss_hnsw.py`](01_faiss_hnsw.py) | locale |
| 02 | FAISS IVF | [`02_faiss_ivf.py`](02_faiss_ivf.py) | locale |
| 03 | Filtres Qdrant | [`03_filtrage_metadonnees.py`](03_filtrage_metadonnees.py) | Qdrant en mémoire |
| 04 | Chroma + embeddings OpenAI | [`04_chroma.py`](04_chroma.py) | `OPENAI_API_KEY` |
| 05 | Collection Qdrant | [`05_qdrant.py`](05_qdrant.py) | Qdrant en mémoire |
| 06 | Pinecone serverless | [`06_pinecone.py`](06_pinecone.py) | `PINECONE_API_KEY` |
| 07 | Self-Query | [`07_self_query.py`](07_self_query.py) | OpenAI |
| 08 | Multi-Query + RRF | [`08_multi_query.py`](08_multi_query.py) | OpenAI |
| 09 | Ensemble BM25 + dense | [`09_ensemble.py`](09_ensemble.py) | locale |
| 10 | Text-to-SQL en lecture seule | [`10_text_to_sql.py`](10_text_to_sql.py) | OpenAI + SQLite |
| 11 | Routeur documents/tables | [`11_router_rag.py`](11_router_rag.py) | OpenAI |
| 12 | Retriever de production | [`12_retriever_production.py`](12_retriever_production.py) | Qdrant + Hugging Face |
| 13 | RAG itératif borné | [`13_rag_iteratif.py`](13_rag_iteratif.py) | OpenAI |
| 14 | RAG adaptatif | [`14_rag_adaptatif.py`](14_rag_adaptatif.py) | OpenAI |

## Installation

```bash
pip install -e ".[vectorstores]"
```

Pour Chroma et Pinecone :

```bash
pip install -e ".[vector-services]"
```

Pour les exemples OpenAI :

```bash
pip install -e ".[openai]"
```

Ne placez jamais une clé directement dans un script ou dans le notebook.
