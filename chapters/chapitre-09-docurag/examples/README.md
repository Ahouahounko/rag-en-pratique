# Exemples du chapitre 9

Ces fichiers proviennent des extraits du manuscrit et ont été transformés en
exemples exécutables. Les étapes qui utilisent un modèle respectent le
fournisseur défini par `RAG_PROVIDER`.

| # | Label LaTeX | Légende | Type | Fichier | Validation |
|---:|---|---|---|---|---|
| 01 | `lst:arborescence` | Arborescence du projet DocuRAG | text | [`01_arborescence.txt`](01_arborescence.txt) | à valider |
| 02 | `lst:config` | \texttt{src/config.py} --- configuration centralisée et typée | python | [`02_config.py`](02_config.py) | syntaxe validée |
| 03 | `lst:env_example` | \texttt{.env.example} --- le modèle à copier, sans aucun secret | text | [`03_env_example.txt`](03_env_example.txt) | à valider |
| 04 | `lst:requirements` | \texttt{requirements.txt} --- dépendances du projet | text | [`04_requirements.txt`](04_requirements.txt) | à valider |
| 05 | `lst:loader` | \texttt{src/ingestion/loader.py} --- chargement multi-sources tolérant | python | [`05_loader.py`](05_loader.py) | syntaxe validée |
| 06 | `lst:chunker` | \texttt{src/ingestion/chunker.py} --- découpage récursif configuré | python | [`06_chunker.py`](06_chunker.py) | syntaxe validée |
| 07 | `lst:indexer` | \texttt{src/ingestion/indexer.py} --- vectorisation et écriture dans Qdrant | python | [`07_indexer.py`](07_indexer.py) | syntaxe validée |
| 08 | `lst:pipeline_ingestion` | \texttt{src/ingestion/\_\_init\_\_.py} --- pipeline complet et incrémental | python | [`08_pipeline_ingestion.py`](08_pipeline_ingestion.py) | syntaxe validée |
| 09 | `lst:retriever` | \texttt{src/retrieval/retriever.py} --- hybride, fusion et re-ranking | python | [`09_retriever.py`](09_retriever.py) | syntaxe validée |
| 10 | `lst:prompts` | \texttt{src/generation/prompts.py} --- gabarits versionnés | python | [`10_prompts.py`](10_prompts.py) | syntaxe validée |
| 11 | `lst:generator` | \texttt{src/generation/generator.py} --- réponse, citations et confiance | python | [`11_generator.py`](11_generator.py) | syntaxe validée |
| 12 | `lst:schemas` | \texttt{src/api/schemas.py} --- contrats d'entrée et de sortie | python | [`12_schemas.py`](12_schemas.py) | syntaxe validée |
| 13 | `lst:api_main` | \texttt{src/api/main.py} --- application FastAPI | python | [`13_api_main.py`](13_api_main.py) | syntaxe validée |
| 14 | `lst:interface` | \texttt{src/interface/app.py} --- interface Streamlit | python | [`14_interface.py`](14_interface.py) | syntaxe validée |
| 15 | `lst:test_evaluation` | \texttt{tests/test\_evaluation.py} --- porte de qualité en intégration continue | python | [`15_test_evaluation.py`](15_test_evaluation.py) | syntaxe validée |
| 16 | `lst:dockerfile` | \texttt{docker/Dockerfile} --- image de l'API | text | [`16_dockerfile.txt`](16_dockerfile.txt) | à valider |
| 17 | `lst:compose` | \texttt{docker/docker-compose.yml} --- la pile complète | yaml | [`17_compose.yml`](17_compose.yml) | à valider |
| 18 | `lst:demarrage` | Séquence de démarrage complète | bash | [`18_demarrage.sh`](18_demarrage.sh) | à valider |

## Convention de validation

- **syntaxe validée** : le fichier Python passe l'analyse syntaxique ;
- **extrait pédagogique** : le bloc est partiel, contient des ellipses ou demande un contexte ;
- **à valider** : commande, configuration, prompt ou autre contenu à tester manuellement.
