# Exemples du chapitre 12

Les six extraits ont été rendus autonomes, injectables et testables sans réseau.

| # | Sujet | Fichier | Résultat |
|---:|---|---|---|
| 01 | Nettoyage | [`01_nettoyage.py`](01_nettoyage.py) | Normalisation conservatrice avant chunking |
| 02 | Test du découpage | [`02_test_decoupage.py`](02_test_decoupage.py) | Comparaison complète/partielle/manquante |
| 03 | Balayage de `k` | [`03_balayage_k.py`](03_balayage_k.py) | Rappel moyen et suggestion du coude |
| 04 | Prompt robuste | [`04_prompt_robuste.txt`](04_prompt_robuste.txt) | Ancrage, refus, citations et délimitation |
| 05 | Journalisation | [`05_journalisation.py`](05_journalisation.py) | Traces structurées avec contenus masqués par défaut |
| 06 | Auto-audit | [`06_audit.py`](06_audit.py) | Constats stables par code et sévérité |

## Journalisation responsable

L'exemple 05 exige une clé HMAC distincte via `RAG_LOG_HMAC_KEY` ou le paramètre
`secret`. Par défaut, il ne conserve que l'empreinte et la longueur des questions
et réponses. Activez `journaliser_contenu=True` uniquement après une décision
explicite concernant la confidentialité, la rétention et les droits d'accès.

Le notebook [`../12_bonnes_pratiques.ipynb`](../12_bonnes_pratiques.ipynb)
reprend chaque exemple et le dossier [`../runnable`](../runnable/) fournit le
runner local.
