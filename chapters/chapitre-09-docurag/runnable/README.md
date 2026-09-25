# DocuRAG exécutable

Cette implémentation reprend l'architecture du chapitre 9 avec deux modes :

- **hors ligne**, actif par défaut et sans clé API ;
- **OpenAI**, facultatif, activé uniquement par `DOCURAG_USE_OPENAI=true`.

Depuis la racine du dépôt, utilisez le notebook Colab ou la commande portable :

```bash
python chapters/chapitre-09-docurag/runnable/run_docurag.py \
  data/sample \
  "Quel est le délai de livraison standard ?"
```

Le mode OpenAI utilise la Responses API pour la génération et l'API embeddings
pour la recherche. Configurez `OPENAI_API_KEY` et `OPENAI_MODEL` seulement au
moment où vous souhaitez l'activer.
