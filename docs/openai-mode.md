# Mode OpenAI facultatif

Les notebooks fonctionnent hors ligne par défaut. Le mode OpenAI n'est activé
que si l'utilisateur positionne explicitement `USE_OPENAI = True` ou
`DOCURAG_USE_OPENAI=true` après avoir configuré son environnement.

## Variables

```text
OPENAI_API_KEY=...
OPENAI_MODEL=...
DOCURAG_USE_OPENAI=true
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
