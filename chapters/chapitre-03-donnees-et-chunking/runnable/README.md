# Parcours exécutable du chapitre 3

Installez les dépendances depuis la racine du dépôt :

```bash
pip install -e ".[chunking]"
```

Puis lancez les quinze démonstrations locales :

```bash
python chapters/chapitre-03-donnees-et-chunking/runnable/run_chapter.py
```

L'exemple 14 est volontairement exclu de ce lancement groupé. Pour tester le
Contextual Retrieval avec OpenAI, configurez `OPENAI_API_KEY` et `OPENAI_MODEL`,
installez `.[openai]`, puis lancez son script séparément.
