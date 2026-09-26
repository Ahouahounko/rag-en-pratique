# DocuRAG exécutable

Cette implémentation reprend l'architecture du chapitre 9 avec un fournisseur
interchangeable : OpenAI, Hugging Face ou Ollama. Configurez `RAG_PROVIDER` et
les variables correspondantes décrites dans [`../../../docs/model-providers.md`](../../../docs/model-providers.md).

Elle ajoute les comportements essentiels du projet :

- empreinte SHA-256 et ingestion incrémentale ;
- recherche dense et lexicale fusionnée par RRF ;
- filtre par métadonnées et seuil d'abstention ;
- réponse citée, sources ordonnées, confiance et version du prompt.

Depuis la racine du dépôt, utilisez le notebook Colab ou la commande portable :

```bash
python chapters/chapitre-09-docurag/runnable/run_docurag.py \
  data/sample \
  "Quel est le délai de livraison standard ?"
```

OpenAI utilise ses API distantes, Hugging Face exécute les modèles localement et
Ollama dialogue avec le serveur local configuré par `OLLAMA_BASE_URL`.

Une seconde ingestion du même dossier renvoie `0` : aucun document inchangé
n'est recalculé. Passez `rebuild=True` dans Python pour reconstruire l'index.
