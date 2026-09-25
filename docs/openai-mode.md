# Configuration OpenAI requise

Les notebooks et scripts RAG utilisent OpenAI pour les embeddings et la
génération. Aucun moteur de substitution hors ligne n'est fourni.

## Variables

```text
OPENAI_API_KEY=...
OPENAI_MODEL=...
```

Ne placez jamais une clé dans un notebook, un fichier suivi par Git ou une
capture d'écran. Le fichier `.env` local est ignoré par le dépôt.

## APIs utilisées

- la [Responses API](https://developers.openai.com/api/docs/guides/text) pour
  produire une réponse fondée sur les passages retrouvés ;
- l'[API embeddings](https://developers.openai.com/api/docs/guides/embeddings)
  avec `text-embedding-3-small` par défaut pour la recherche vectorielle.

Le modèle de génération n'est volontairement pas inscrit en dur : renseignez
`OPENAI_MODEL` avec un modèle auquel votre projet OpenAI a accès au moment de
l'exécution.
