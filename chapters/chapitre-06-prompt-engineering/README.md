# Chapitre 6 — Prompt engineering pour le RAG

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/blob/main/chapters/chapitre-06-prompt-engineering/06_prompt_engineering.ipynb)

Ce chapitre montre comment construire, structurer, vérifier et tester les
prompts employés dans un système RAG.

## Contenu

- [`06_prompt_engineering.ipynb`](06_prompt_engineering.ipynb) : parcours pédagogique Colab ;
- [`examples/`](examples/) : 17 scripts correspondant aux extraits du manuscrit ;
- [`runnable/`](runnable/) : démonstrations locales sans appel API.

## Ressources officielles

- [OpenAI Docs — Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [OpenAI Docs — Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [OpenAI Docs — Bonnes pratiques de sécurité](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [tiktoken](https://github.com/openai/tiktoken)

Les exemples OpenAI utilisent la Responses API avec une variable
`OPENAI_MODEL` explicite. La clé peut être saisie de manière masquée dans le
notebook et n'est jamais écrite dans celui-ci.
