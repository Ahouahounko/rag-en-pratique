# Exécuter le chapitre 5

Depuis la racine du dépôt :

```bash
pip install -e ".[vectorstores]"
python chapters/chapitre-05-bases-vectorielles/runnable/run_chapter.py
```

Cette commande exécute uniquement les démonstrations locales. Les exemples
OpenAI, Chroma et Pinecone restent indépendants afin d'éviter tout appel distant
accidentel. Pour les essayer, installez les extras concernés et configurez les
variables indiquées dans le notebook.
