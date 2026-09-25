# Exemples du chapitre 3

Les fichiers de ce dossier sont extraits automatiquement du manuscrit. 
Le contenu est conservé tel quel afin de permettre sa revue avant transformation 
en exemple autonome ou en notebook exécutable.

| # | Label LaTeX | Légende | Type | Fichier | Validation |
|---:|---|---|---|---|---|
| 01 | `lst:comptage_tokens` | Mesurer en tokens, pas en caractères — et vérifier le biais de langue | python | [`01_comptage_tokens.py`](01_comptage_tokens.py) | syntaxe validée |
| 02 | `lst:validation_taille` | Garde-fou : valider la taille avant vectorisation | python | [`02_validation_taille.py`](02_validation_taille.py) | syntaxe validée |
| 03 | `lst:fusion_overlap` | Fusion des chunks chevauchants après récupération | python | [`03_fusion_overlap.py`](03_fusion_overlap.py) | syntaxe validée |
| 04 | `lst:chunking_fixe` | Découpage à taille fixe --- la ligne de base | python | [`04_chunking_fixe.py`](04_chunking_fixe.py) | syntaxe validée |
| 05 | `lst:mecanisme_recursif` | Le mécanisme récursif, en pseudo-code | text | [`05_mecanisme_recursif.txt`](05_mecanisme_recursif.txt) | à valider |
| 06 | `lst:chunking_recursif` | Découpage récursif --- le réglage qui change tout | python | [`06_chunking_recursif.py`](06_chunking_recursif.py) | syntaxe validée |
| 07 | `lst:cartographie` | Phase 1 — Cartographier avant de découper | python | [`07_cartographie.py`](07_cartographie.py) | syntaxe validée |
| 08 | `lst:context_prepending` | Phase 3 — L'objet de données immuable et le Context Prepending | python | [`08_context_prepending.py`](08_context_prepending.py) | syntaxe validée |
| 09 | `lst:chunking_ast` | Découpage de code par frontières syntaxiques | python | [`09_chunking_ast.py`](09_chunking_ast.py) | syntaxe validée |
| 10 | `lst:chunking_tableaux` | Chunking des tableaux avec Chonkie --- un tableau reste une unité | python | [`10_chunking_tableaux.py`](10_chunking_tableaux.py) | syntaxe validée |
| 11 | `lst:chunking_semantique` | Chunking sémantique par détection de ruptures | python | [`11_chunking_semantique.py`](11_chunking_semantique.py) | syntaxe validée |
| 12 | `lst:semantique_accumulation` | Détection de rupture par accumulation, en pseudo-code | text | [`12_semantique_accumulation.txt`](12_semantique_accumulation.txt) | à valider |
| 13 | `lst:parent_child` | La logique Parent-Child, en Python exécutable | python | [`13_parent_child.py`](13_parent_child.py) | syntaxe validée |
| 14 | `lst:contextual_retrieval` | Pseudo-code — Contextual Retrieval à l'ingestion | python | [`14_contextual_retrieval.py`](14_contextual_retrieval.py) | syntaxe validée |
| 15 | `lst:late_chunking` | Late Chunking --- vectorisation globale avant découpage, exemple complet | python | [`15_late_chunking.py`](15_late_chunking.py) | syntaxe validée |
| 16 | `lst:grid_search` | Pseudo-code — exploration systématique des réglages | python | [`16_grid_search.py`](16_grid_search.py) | syntaxe validée |

## Convention de validation

- **syntaxe validée** : le fichier Python passe l'analyse syntaxique ;
- **extrait pédagogique** : le bloc est partiel, contient des ellipses ou demande un contexte ;
- **à valider** : commande, configuration, prompt ou autre contenu à tester manuellement.
