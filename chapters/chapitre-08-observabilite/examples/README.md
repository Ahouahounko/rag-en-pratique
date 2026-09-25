# Exemples du chapitre 8

Les fichiers de ce dossier sont extraits automatiquement du manuscrit. 
Le contenu est conservé tel quel afin de permettre sa revue avant transformation 
en exemple autonome ou en notebook exécutable.

| # | Label LaTeX | Légende | Type | Fichier | Validation |
|---:|---|---|---|---|---|
| 01 | `lst:generation_jeu` | Génération d'un jeu de référence, en pseudo-code | text | [`01_generation_jeu.txt`](01_generation_jeu.txt) | à valider |
| 02 | `lst:questions_discriminantes` | Génération de questions discriminantes avec distracteurs | python | [`02_questions_discriminantes.py`](02_questions_discriminantes.py) | syntaxe validée |
| 03 | `lst:filtrage_questions` | Filtrage des questions synthétiques par notation guidée | python | [`03_filtrage_questions.py`](03_filtrage_questions.py) | syntaxe validée |
| 04 | `lst:prompt_juge` | Prompt de juge structuré pour la \textit{faithfulness} | python | [`04_prompt_juge.py`](04_prompt_juge.py) | syntaxe validée |
| 05 | `lst:execution_juge` | Exécution du juge et extraction du verdict | python | [`05_execution_juge.py`](05_execution_juge.py) | syntaxe validée |
| 06 | `lst:deux_outils` | Deux philosophies : campagne de mesure et test de non-régression | python | [`06_deux_outils.py`](06_deux_outils.py) | syntaxe validée |
| 07 | `lst:matrice_attribution` | Matrice d'attribution des défaillances par composant | python | [`07_matrice_attribution.py`](07_matrice_attribution.py) | syntaxe validée |
| 08 | `lst:substitution_contexte` | Test de substitution de contexte | python | [`08_substitution_contexte.py`](08_substitution_contexte.py) | syntaxe validée |
| 09 | `lst:percentiles` | Suivi des percentiles de latence par étape | python | [`09_percentiles.py`](09_percentiles.py) | syntaxe validée |
| 10 | `lst:detection_drift` | Détection de dérive sur les métriques de qualité | python | [`10_detection_drift.py`](10_detection_drift.py) | syntaxe validée |

## Convention de validation

- **syntaxe validée** : le fichier Python passe l'analyse syntaxique ;
- **extrait pédagogique** : le bloc est partiel, contient des ellipses ou demande un contexte ;
- **à valider** : commande, configuration, prompt ou autre contenu à tester manuellement.
