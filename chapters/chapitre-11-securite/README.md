# Chapitre 11 — Sécurité et fiabilité

Défendre un système RAG contre les injections indirectes, appliquer les droits
d'accès et d'effacement, puis mesurer les changements sans fausser les résultats.

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/blob/main/chapters/chapitre-11-securite/11_securite.ipynb)

## Parcours exécutable

- [`11_securite.ipynb`](11_securite.ipynb) : les six exemples expliqués ;
- [`examples`](examples/) : filtres, ACL, effacement et tests A/B ;
- [`runnable/run_chapter.py`](runnable/run_chapter.py) : démonstrations locales sans appel distant.

## Ressources officielles

- [OpenAI Docs — Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenAI Docs — Moderation](https://developers.openai.com/api/docs/guides/moderation)
- [OWASP — Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [CNIL — droit à l'effacement](https://www.cnil.fr/fr/le-droit-leffacement-supprimer-vos-donnees-en-ligne)

> Le filtre d'injection est une couche de détection, pas une garantie. Les ACL
> doivent être appliquées avant le retrieval, et les actions accessibles au
> modèle doivent rester limitées et contrôlées côté serveur.

## Code du manuscrit

Ce chapitre contient **6 blocs de code** issus du manuscrit. Consultez
[l'inventaire des exemples](examples/README.md).
