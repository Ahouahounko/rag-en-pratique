# Exemples du chapitre 11

Les six extraits ont été transformés en composants testables et orientés vers
un comportement sûr par défaut.

| # | Sujet | Fichier | Garantie recherchée |
|---:|---|---|---|
| 01 | Filtre d'injection | [`01_filtre_injection.py`](01_filtre_injection.py) | Normalisation et quarantaine, sans suppression automatique |
| 02 | Séparation du contexte | [`02_separation_contexte.txt`](02_separation_contexte.txt) | Distinguer instructions, données externes et question |
| 03 | Retrieval avec ACL | [`03_retrieval_acl.py`](03_retrieval_acl.py) | Échouer fermé et filtrer avant similarité |
| 04 | Droit à l'effacement | [`04_droit_effacement.py`](04_droit_effacement.py) | Purger toutes les couches sans journaliser l'identifiant |
| 05 | Framework A/B | [`05_ab_framework.py`](05_ab_framework.py) | Assignation stable, test de Welch et effet minimal |
| 06 | Taille d'échantillon | [`06_taille_echantillon.py`](06_taille_echantillon.py) | Fixer l'effectif avant d'observer les résultats |

## Ordre de défense recommandé

1. authentifier l'utilisateur et déterminer ses rôles ;
2. appliquer les ACL dans la requête adressée à l'index ;
3. contrôler et mettre en quarantaine les sources suspectes ;
4. séparer clairement instructions et données ;
5. limiter les outils et actions autorisés côté serveur ;
6. surveiller les sorties et exécuter régulièrement des tests adversariaux.

Le notebook [`../11_securite.ipynb`](../11_securite.ipynb) reprend les exemples
dans cet ordre et le dossier [`../runnable`](../runnable/) fournit un runner local.
