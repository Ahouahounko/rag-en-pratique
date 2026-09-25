# Choisir le fournisseur de modèles

Les notebooks et scripts des chapitres 2 et 9 partagent la même variable :

```text
RAG_PROVIDER=openai
```

Les valeurs acceptées sont `openai`, `huggingface` et `ollama`. Le retrieval,
le chunking et les citations ne changent pas : seuls les adaptateurs d'embeddings
et de génération sont remplacés.

## OpenAI

Installation et configuration :

```bash
pip install -e ".[openai]"
```

```text
RAG_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_MODEL=...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

La clé doit rester dans l'environnement ou dans un fichier `.env` non versionné.
Le code utilise la [Responses API](https://developers.openai.com/api/docs/guides/text)
et l'[API embeddings](https://developers.openai.com/api/docs/guides/embeddings).

## Hugging Face

Installation et configuration :

```bash
pip install -e ".[huggingface]"
```

```text
RAG_PROVIDER=huggingface
HF_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
HF_GENERATION_MODEL=Qwen/Qwen2.5-0.5B-Instruct
HF_MAX_NEW_TOKENS=256
```

Les modèles sont téléchargés depuis le Hub au premier lancement. Ce mode est
adapté à Colab et à une machine locale ; activez un GPU Colab pour accélérer la
génération. Certains modèles du Hub peuvent demander une acceptation de licence
ou un jeton Hugging Face : les valeurs par défaut ci-dessus sont publiques.

## Ollama

Installez Ollama sur la machine, puis préparez les modèles :

```bash
ollama pull embeddinggemma
ollama pull qwen3:0.6b
```

```text
RAG_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=embeddinggemma
OLLAMA_MODEL=qwen3:0.6b
```

Ce mode vise Jupyter en local. Un notebook Colab distant ne peut normalement
pas joindre le serveur Ollama de votre ordinateur sans configuration réseau
supplémentaire. L'adaptateur appelle les endpoints officiels `/api/embed` et
`/api/chat`.

## Lancer un exemple

Après avoir choisi et configuré un fournisseur :

```bash
python chapters/chapitre-02-premier-rag/runnable/premier_rag.py
python chapters/chapitre-09-docurag/runnable/run_docurag.py data/sample "Quel est le délai de livraison ?"
```
