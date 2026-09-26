# Exemples du chapitre 9

Les 18 extraits du manuscrit forment ici un parcours cohérent. Les scripts Python
peuvent être lancés depuis la racine du dépôt ; les fichiers d'infrastructure sont
des modèles prêts à adapter pour un déploiement persistant avec Qdrant.

| # | Sujet | Fichier | Rôle |
|---:|---|---|---|
| 01 | Arborescence | [`01_arborescence.txt`](01_arborescence.txt) | Séparer ingestion, retrieval, génération et interfaces |
| 02 | Configuration | [`02_config.py`](02_config.py) | Lire et valider les variables d'environnement |
| 03 | Environnement | [`03_env_example.txt`](03_env_example.txt) | Documenter les variables sans stocker de secret |
| 04 | Dépendances | [`04_requirements.txt`](04_requirements.txt) | Choisir les extras d'installation |
| 05 | Loader | [`05_loader.py`](05_loader.py) | Charger les textes, enrichir les métadonnées et calculer une empreinte |
| 06 | Chunker | [`06_chunker.py`](06_chunker.py) | Découper en conservant source et position |
| 07 | Indexeur | [`07_indexer.py`](07_indexer.py) | Vectoriser avec le fournisseur configuré |
| 08 | Ingestion | [`08_pipeline_ingestion.py`](08_pipeline_ingestion.py) | Assembler découpage et indexation |
| 09 | Retriever | [`09_retriever.py`](09_retriever.py) | Fusionner classements dense et lexical avec RRF |
| 10 | Prompts | [`10_prompts.py`](10_prompts.py) | Versionner ancrage, citations et abstention |
| 11 | Générateur | [`11_generator.py`](11_generator.py) | Produire réponse, sources et confiance |
| 12 | Schémas | [`12_schemas.py`](12_schemas.py) | Définir les contrats Pydantic |
| 13 | API | [`13_api_main.py`](13_api_main.py) | Exposer santé, ingestion et interrogation |
| 14 | Interface | [`14_interface.py`](14_interface.py) | Afficher réponse, confiance, latence et sources |
| 15 | Évaluation | [`15_test_evaluation.py`](15_test_evaluation.py) | Juger l'ancrage et bloquer les régressions |
| 16 | Dockerfile | [`16_dockerfile.txt`](16_dockerfile.txt) | Construire l'image de l'API |
| 17 | Compose | [`17_compose.yml`](17_compose.yml) | Orchestrer Qdrant, API et interface |
| 18 | Démarrage | [`18_demarrage.sh`](18_demarrage.sh) | Lancer la pile et les ingestions |

## Fournisseurs

Les scripts 07, 08, 09, 11, 13 et 15 utilisent le fournisseur indiqué par
`RAG_PROVIDER` :

```bash
pip install -e ".[openai]"       # API OpenAI
pip install -e ".[huggingface]"  # modèles locaux ou Colab
pip install -e .                  # Ollama via son serveur local
```

OpenAI nécessite `OPENAI_API_KEY`, `OPENAI_MODEL` et éventuellement
`OPENAI_EMBEDDING_MODEL`. Aucune clé n'est incluse dans le dépôt.

## Exécution intégrée

Le dossier [`../runnable`](../runnable/) assemble ces concepts dans une
application testable. Le notebook [`../09_docurag.ipynb`](../09_docurag.ipynb)
reprend les 18 étapes dans le même ordre.
