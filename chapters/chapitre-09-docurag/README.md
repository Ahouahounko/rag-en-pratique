# Chapitre 9 — DocuRAG

Projet fil rouge assemblant un système RAG complet, testable et utilisable.

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/blob/main/chapters/chapitre-09-docurag/09_docurag.ipynb)

## Parcours exécutable

- [`09_docurag.ipynb`](09_docurag.ipynb) : les 18 extraits expliqués dans l'ordre du chapitre ;
- [`examples`](examples/) : scripts autonomes, contrats et fichiers de déploiement ;
- [`runnable/docurag`](runnable/docurag/) : application Python modulaire avec ingestion incrémentale,
  retrieval hybride, abstention, citations et confiance ;
- [`runnable/run_docurag.py`](runnable/run_docurag.py) : point d'entrée local ;
- OpenAI, Hugging Face et Ollama sont proposés pour les embeddings et la génération.

## Démarrage rapide

```bash
pip install -e ".[openai,app,pdf,retrieval]"
export RAG_PROVIDER=openai
export OPENAI_API_KEY="..."
export OPENAI_MODEL="votre-modele"
python chapters/chapitre-09-docurag/runnable/run_docurag.py \
  data/sample "Quel est le délai de livraison standard ?"
```

Sous PowerShell, utilisez `$env:NOM_VARIABLE="valeur"` à la place de `export`.

## Ressources

- [OpenAI Docs — génération de texte](https://developers.openai.com/api/docs/guides/text-generation)
- [OpenAI Docs — embeddings](https://developers.openai.com/api/docs/guides/embeddings)
- [Qdrant](https://qdrant.tech/documentation/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://docs.streamlit.io/)

## Code du manuscrit

Ce chapitre contient **18 blocs de code** issus du manuscrit. Consultez [l'inventaire des exemples](examples/README.md).
