# RAG en pratique

Dépôt compagnon du livre consacré à la conception de systèmes de
Retrieval-Augmented Generation (RAG), des fondations jusqu'à la production.

> Le dépôt est actuellement public afin de rendre les exemples et les liens
> Google Colab directement accessibles.

## Ce que contient le dépôt

- des notebooks exécutables associés aux douze chapitres ;
- les exemples Python présentés dans le livre ;
- des exercices et leurs solutions ;
- des données de démonstration libres ou synthétiques ;
- des tests garantissant que les exemples restent fonctionnels ;
- le projet fil rouge **DocuRAG**.

Le manuscrit, le PDF, la couverture et les illustrations du livre ne font pas
partie de ce dépôt.

## Parcours par chapitre

| # | Chapitre | Dossier |
|---:|---|---|
| 1 | IA générative et grands modèles de langage | [`chapitre-01-fondations-llm`](chapters/chapitre-01-fondations-llm/) |
| 2 | Introduction au RAG et premier RAG naïf | [`chapitre-02-premier-rag`](chapters/chapitre-02-premier-rag/) |
| 3 | Préparation des données et chunking avancé | [`chapitre-03-donnees-et-chunking`](chapters/chapitre-03-donnees-et-chunking/) |
| 4 | Retrieval avancé | [`chapitre-04-retrieval-avance`](chapters/chapitre-04-retrieval-avance/) |
| 5 | Bases vectorielles et architectures de retrieval | [`chapitre-05-bases-vectorielles`](chapters/chapitre-05-bases-vectorielles/) |
| 6 | Prompt engineering pour le RAG | [`chapitre-06-prompt-engineering`](chapters/chapitre-06-prompt-engineering/) |
| 7 | Cadrage de l'évaluation et métriques | [`chapitre-07-evaluation`](chapters/chapitre-07-evaluation/) |
| 8 | Mesure, diagnostic et surveillance | [`chapitre-08-observabilite`](chapters/chapitre-08-observabilite/) |
| 9 | DocuRAG : construire un système complet | [`chapitre-09-docurag`](chapters/chapitre-09-docurag/) |
| 10 | Latence, coûts et scalabilité | [`chapitre-10-optimisation`](chapters/chapitre-10-optimisation/) |
| 11 | Sécurité et fiabilité | [`chapitre-11-securite`](chapters/chapitre-11-securite/) |
| 12 | Bonnes pratiques | [`chapitre-12-bonnes-pratiques`](chapters/chapitre-12-bonnes-pratiques/) |

## Installation locale

Prérequis : Python 3.11 ou 3.12.

```bash
git clone https://github.com/Ahouahounko/rag-en-pratique.git
cd rag-en-pratique
python -m venv .venv
```

Activation de l'environnement :

```bash
# macOS et Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Installation :

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Copiez `.env.example` vers `.env`, puis renseignez uniquement les services que
vous souhaitez utiliser. Ne publiez jamais le fichier `.env`.

## Exécution

```bash
jupyter lab
```

Les exemples RAG acceptent OpenAI, Hugging Face ou Ollama. Configurez
`RAG_PROVIDER`, puis uniquement les variables du fournisseur choisi.

## Notebooks disponibles

- [Chapitre 2 — Premier RAG](chapters/chapitre-02-premier-rag/02_premier_rag.ipynb) :
  ingestion, chunking, indexation, retrieval et citations ;
- [Chapitre 3 — Données et chunking](chapters/chapitre-03-donnees-et-chunking/03_donnees_et_chunking.ipynb) :
  16 expériences sur les stratégies de découpage et leurs métadonnées ;
- [Chapitre 4 — Retrieval avancé](chapters/chapitre-04-retrieval-avance/04_retrieval_avance.ipynb) :
  réécriture, expansion, HyDE, recherche hybride, reranking, MMR et compression ;
- [Chapitre 5 — Bases vectorielles](chapters/chapitre-05-bases-vectorielles/05_bases_vectorielles.ipynb) :
  FAISS, Qdrant, Chroma, Pinecone et architectures de retrieval ;
- [Chapitre 6 — Prompt engineering](chapters/chapitre-06-prompt-engineering/06_prompt_engineering.ipynb) :
  contexte, citations, refus, conversation, synthèse et tests de régression ;
- [Chapitre 9 — DocuRAG](chapters/chapitre-09-docurag/09_docurag.ipynb) :
  application modulaire et parcours complet.

Ces notebooks proposent un sélecteur OpenAI, Hugging Face ou Ollama. Consultez
[le guide des fournisseurs](docs/model-providers.md).

## Tests

```bash
pytest
```

## Statut

Les **111 blocs de code** du manuscrit sont désormais extraits et classés par
chapitre. Parmi eux, 96 exemples Python passent une première validation
syntaxique ; les 15 autres blocs correspondent à des commandes, configurations
ou prompts à valider manuellement. Consultez le
[catalogue du code](docs/code-inventory.md) pour accéder aux inventaires.

## Droits

Tous droits réservés pendant la phase privée. Une licence MIT couvrant le code
sera ajoutée lors de l'ouverture publique. Le contenu éditorial du livre restera
protégé séparément.
