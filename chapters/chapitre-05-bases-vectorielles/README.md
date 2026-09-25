# Chapitre 5 — Bases vectorielles

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/blob/main/chapters/chapitre-05-bases-vectorielles/05_bases_vectorielles.ipynb)

Ce chapitre couvre l'indexation vectorielle, le filtrage par métadonnées et les
architectures de retrieval qui combinent plusieurs sources ou plusieurs étapes.

## Contenu

- [`05_bases_vectorielles.ipynb`](05_bases_vectorielles.ipynb) : parcours pédagogique Colab ;
- [`examples/`](examples/) : 14 scripts autonomes correspondant au manuscrit ;
- [`runnable/`](runnable/) : lanceur des démonstrations locales sans appel distant.

## Ressources officielles

- [FAISS](https://faiss.ai/)
- [Qdrant — documentation](https://qdrant.tech/documentation/)
- [Chroma — documentation](https://docs.trychroma.com/)
- [Pinecone — documentation](https://docs.pinecone.io/)
- [OpenAI — embeddings](https://developers.openai.com/api/docs/guides/embeddings)
- [Sentence Transformers — Retrieve & Re-Rank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

Les services externes ne sont jamais appelés par le lanceur local. Le notebook
indique clairement les cellules qui nécessitent une clé OpenAI ou Pinecone.
