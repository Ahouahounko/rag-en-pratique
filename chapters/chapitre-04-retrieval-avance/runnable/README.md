# Parcours exécutable du chapitre 4

Depuis la racine du dépôt :

```bash
pip install -e ".[retrieval]"
python chapters/chapitre-04-retrieval-avance/runnable/run_chapter.py
```

Pour inclure le reranker Hugging Face, qui télécharge le modèle public lors du
premier lancement :

```bash
pip install -e ".[retrieval,huggingface]"
python chapters/chapitre-04-retrieval-avance/runnable/run_chapter.py --avec-huggingface
```

Les scripts 1, 2, 3 et 9 n'appellent OpenAI que si `OPENAI_API_KEY` et
`OPENAI_MODEL` sont configurés. Le lancement par défaut ne réalise donc aucun
appel distant.
