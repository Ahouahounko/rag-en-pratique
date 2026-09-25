# Exemples du chapitre 12

Les fichiers de ce dossier sont extraits automatiquement du manuscrit. 
Le contenu est conservé tel quel afin de permettre sa revue avant transformation 
en exemple autonome ou en notebook exécutable.

| # | Label LaTeX | Légende | Type | Fichier | Validation |
|---:|---|---|---|---|---|
| 01 | `lst:nettoyage` | Fonction de nettoyage de base avant chunking | python | [`01_nettoyage.py`](01_nettoyage.py) | syntaxe validée |
| 02 | `lst:test_decoupage` | Harnais de test du découpage sur de vraies questions | python | [`02_test_decoupage.py`](02_test_decoupage.py) | syntaxe validée |
| 03 | `lst:balayage_k` | Balayage de $k$ sur le jeu de référence | python | [`03_balayage_k.py`](03_balayage_k.py) | syntaxe validée |
| 04 | `lst:prompt_robuste` | Prompt système comportant les trois clauses | text | [`04_prompt_robuste.txt`](04_prompt_robuste.txt) | à valider |
| 05 | `lst:journalisation` | Journalisation structurée d'une requête complète | python | [`05_journalisation.py`](05_journalisation.py) | syntaxe validée |
| 06 | `lst:audit` | Script d'auto-audit contre les anti-patterns vérifiables à froid | python | [`06_audit.py`](06_audit.py) | syntaxe validée |

## Convention de validation

- **syntaxe validée** : le fichier Python passe l'analyse syntaxique ;
- **extrait pédagogique** : le bloc est partiel, contient des ellipses ou demande un contexte ;
- **à valider** : commande, configuration, prompt ou autre contenu à tester manuellement.
