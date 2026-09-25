# Exemples du chapitre 8

| # | Sujet | Fichier | Exécution |
|---:|---|---|---|
| 01 | Génération d'un jeu de référence | [`01_generation_jeu.py`](01_generation_jeu.py) | OpenAI facultatif |
| 02 | Questions discriminantes | [`02_questions_discriminantes.py`](02_questions_discriminantes.py) | OpenAI facultatif |
| 03 | Filtrage par réalisme | [`03_filtrage_questions.py`](03_filtrage_questions.py) | OpenAI facultatif |
| 04 | Prompt du juge | [`04_prompt_juge.py`](04_prompt_juge.py) | locale |
| 05 | Exécution du juge | [`05_execution_juge.py`](05_execution_juge.py) | OpenAI facultatif |
| 06 | Campagne et non-régression | [`06_deux_outils.py`](06_deux_outils.py) | locale |
| 07 | Matrice d'attribution | [`07_matrice_attribution.py`](07_matrice_attribution.py) | juge injectable |
| 08 | Substitution de contexte | [`08_substitution_contexte.py`](08_substitution_contexte.py) | locale |
| 09 | Percentiles de latence | [`09_percentiles.py`](09_percentiles.py) | locale |
| 10 | Détection de dérive | [`10_detection_drift.py`](10_detection_drift.py) | locale |

Le pseudo-code numéro 1 a été remplacé par un générateur Python avec répartition
contrôlée des questions directes, de synthèse et sans réponse.

## Installation

```bash
pip install -e ".[observability]"
```

Pour les exemples utilisant OpenAI :

```bash
pip install -e ".[openai]"
```
