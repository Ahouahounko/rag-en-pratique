# Configuration OpenAI

OpenAI est l'un des trois fournisseurs disponibles. Consultez le
[guide multi-fournisseur](model-providers.md) pour choisir entre OpenAI,
Hugging Face et Ollama.

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

Le modèle de génération n'est volontairement pas imposé : renseignez
`OPENAI_MODEL` avec un modèle auquel votre projet OpenAI a accès au moment de
l'exécution.
