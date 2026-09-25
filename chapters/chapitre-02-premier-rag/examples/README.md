# Exemples du chapitre 2

Ces fichiers proviennent des extraits du manuscrit et ont été transformés en
exemples exécutables. Les étapes qui utilisent un modèle respectent le
fournisseur défini par `RAG_PROVIDER`.

| # | Label LaTeX | Légende | Type | Fichier | Validation |
|---:|---|---|---|---|---|
| 01 | `lst:document_loading` | Chargement de documents selon leur format d'origine | python | [`01_document_loading.py`](01_document_loading.py) | syntaxe validée |
| 02 | `lst:pipeline_ingestion` | Pipeline d'ingestion complet : du document à la base vectorielle | python | [`02_pipeline_ingestion.py`](02_pipeline_ingestion.py) | syntaxe validée |
| 03 | `lst:generator_rag` | Generator RAG avec prompt de grounding et instruction de citation | python | [`03_generator_rag.py`](03_generator_rag.py) | syntaxe validée |
| 04 | `lst:naive_rag_complet` | Pipeline RAG naif complet : de la question à la réponse sourcée | python | [`04_naive_rag_complet.py`](04_naive_rag_complet.py) | syntaxe validée |

## Convention de validation

- **syntaxe validée** : le fichier Python passe l'analyse syntaxique ;
- **extrait pédagogique** : le bloc est partiel, contient des ellipses ou demande un contexte ;
- **à valider** : commande, configuration, prompt ou autre contenu à tester manuellement.
