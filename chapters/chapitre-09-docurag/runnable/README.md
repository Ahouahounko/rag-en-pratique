# DocuRAG exécutable

Cette implémentation reprend l'architecture du chapitre 9 avec OpenAI pour les
embeddings et la génération. `OPENAI_API_KEY` et `OPENAI_MODEL` sont requis.

Depuis la racine du dépôt, utilisez le notebook Colab ou la commande portable :

```bash
python chapters/chapitre-09-docurag/runnable/run_docurag.py \
  data/sample \
  "Quel est le délai de livraison standard ?"
```

DocuRAG utilise la Responses API pour la génération et l'API embeddings pour la
recherche. Configurez `OPENAI_API_KEY` et `OPENAI_MODEL` avant l'exécution.
