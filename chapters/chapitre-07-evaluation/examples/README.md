# Exemples du chapitre 7

| # | Sujet | Fichier | Exécution |
|---:|---|---|---|
| 01 | Hit Rate, Precision@k, Recall@k, MRR et nDCG | [`01_metriques_rang.py`](01_metriques_rang.py) | locale |
| 02 | nDCG à pertinence graduée | [`02_ndcg_gradue.py`](02_ndcg_gradue.py) | locale |
| 03 | Fidélité détaillée | [`03_fidelite_maison.py`](03_fidelite_maison.py) | OpenAI facultatif |
| 04 | Campagne et diagnostic | [`04_campagne_evaluation.py`](04_campagne_evaluation.py) | local + juge injectable |

## Exécution

```bash
python chapters/chapitre-07-evaluation/runnable/run_chapter.py
```

Pour utiliser OpenAI comme juge :

```bash
pip install -e ".[openai]"
```

Les fonctions acceptent un client injecté, ce qui permet de tester toute la
logique sans appel payant.
