"""Construit les notebooks Colab sans dépendre de nbformat."""

from __future__ import annotations

import json
from pathlib import Path

REPOSITORY_URL = "https://github.com/Ahouahounko/rag-en-pratique"
ROOT = Path(__file__).resolve().parents[1]


def markdown(source: str) -> dict[str, object]:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict[str, object]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def notebook(cells: list[dict[str, object]]) -> dict[str, object]:
    return {
        "cells": cells,
        "metadata": {
            "colab": {"name": "RAG en pratique", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


PROVIDER_SELECTION = '''# @title Choisir le fournisseur de modèles
PROVIDER = "openai" # @param ["openai", "huggingface", "ollama"]
PROVIDER = PROVIDER.strip().lower()
if PROVIDER not in {"openai", "huggingface", "ollama"}:
    raise ValueError("Choisissez openai, huggingface ou ollama")
print("Fournisseur choisi :", PROVIDER)
'''

BOOTSTRAP = f'''import os
import subprocess
import sys
from pathlib import Path

if not Path("src").is_dir():
    if not Path("rag-en-pratique").is_dir():
        subprocess.run(["git", "clone", "{REPOSITORY_URL}.git"], check=True)
    os.chdir("rag-en-pratique")

sys.path.insert(0, str(Path("src").resolve()))
extra = {{"openai": "openai", "huggingface": "huggingface", "ollama": None}}[PROVIDER]
target = f".[{{extra}}]" if extra else "."
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-e", target], check=True)
print("Dépôt prêt :", Path.cwd())
'''

PROVIDER_SETUP = '''import os
from getpass import getpass

os.environ["RAG_PROVIDER"] = PROVIDER
if PROVIDER == "openai":
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass("OPENAI_API_KEY : ")
    if not os.getenv("OPENAI_MODEL"):
        os.environ["OPENAI_MODEL"] = input("OPENAI_MODEL : ").strip()
    if not os.environ["OPENAI_API_KEY"] or not os.environ["OPENAI_MODEL"]:
        raise RuntimeError("OPENAI_API_KEY et OPENAI_MODEL sont obligatoires")
elif PROVIDER == "huggingface":
    os.environ.setdefault(
        "HF_EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    os.environ.setdefault("HF_GENERATION_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
else:
    os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434")
    os.environ.setdefault("OLLAMA_EMBEDDING_MODEL", "embeddinggemma")
    os.environ.setdefault("OLLAMA_MODEL", "qwen3:0.6b")
    print("Ollama doit déjà être démarré et les deux modèles téléchargés.")
print("Configuration chargée pour", PROVIDER)
'''

CHAPTER_3_BOOTSTRAP = f'''import os
import subprocess
import sys
from pathlib import Path

if not Path("src").is_dir():
    if not Path("rag-en-pratique").is_dir():
        subprocess.run(["git", "clone", "{REPOSITORY_URL}.git"], check=True)
    os.chdir("rag-en-pratique")

subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "-e", ".[chunking]"],
    check=True,
)
print("Environnement du chapitre 3 prêt :", Path.cwd())
'''

CHAPTER_3_OPENAI = '''# @title Exemple 14 — activer OpenAI seulement si vous avez une clé
UTILISER_OPENAI = False # @param {type:"boolean"}

if UTILISER_OPENAI:
    import os
    import subprocess
    import sys
    from getpass import getpass

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-e", ".[openai]"],
        check=True,
    )
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass("OPENAI_API_KEY : ")
    if not os.getenv("OPENAI_MODEL"):
        os.environ["OPENAI_MODEL"] = input("OPENAI_MODEL : ").strip()
    print("OpenAI est prêt pour l'exemple 14.")
else:
    print("OpenAI désactivé : tous les autres exemples restent exécutables.")
'''


def chapter_3() -> dict[str, object]:
    badge = (
        "https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/"
        "blob/main/chapters/chapitre-03-donnees-et-chunking/03_donnees_et_chunking.ipynb"
    )
    examples = ROOT / "chapters/chapitre-03-donnees-et-chunking/examples"
    lessons = [
        ("01_comptage_tokens.py", "Compter les tokens", "Comparer caractères et tokens avant tout découpage."),
        ("02_validation_taille.py", "Valider les tailles", "Détecter les chunks qui dépasseraient le budget."),
        ("03_fusion_overlap.py", "Fusionner les chevauchements", "Reconstruire un passage sans répéter l'overlap."),
        ("04_chunking_fixe.py", "Ligne de base fixe", "Établir une référence simple avant les stratégies avancées."),
        ("05_mecanisme_recursif.py", "Comprendre la récursion", "Passer progressivement des grandes frontières aux petites."),
        ("06_chunking_recursif.py", "Respecter Markdown", "Prioriser sections, paragraphes, phrases puis mots."),
        ("07_cartographie.py", "Cartographier le document", "Conserver le chemin hiérarchique de chaque section."),
        ("08_context_prepending.py", "Ajouter le contexte", "Distinguer le texte vectorisé des métadonnées stockées."),
        ("09_chunking_ast.py", "Découper du code Python", "Préserver fonctions, classes, imports et numéros de ligne."),
        ("10_chunking_tableaux.py", "Préserver les tableaux", "Répéter l'en-tête pour que chaque fragment reste lisible."),
        ("11_chunking_semantique.py", "Détecter les ruptures", "Utiliser un embedding TF-IDF local et explicable."),
        ("12_semantique_accumulation.py", "Accumuler par cohérence", "Comparer chaque segment au centre du chunk courant."),
        ("13_parent_child.py", "Indexation Parent-Child", "Chercher des enfants précis et restituer leurs parents."),
        ("14_contextual_retrieval.py", "Contextual Retrieval", "Seul exemple facultatif qui appelle OpenAI."),
        ("15_late_chunking.py", "Late Chunking", "Découper les vecteurs après encodage global."),
        ("16_grid_search.py", "Comparer les réglages", "Évaluer plusieurs tailles, overlaps et stratégies."),
    ]
    cells = [
        markdown(
            f"# Chapitre 3 — Données et chunking\n\n"
            f"[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge})\n\n"
            "Ce laboratoire transforme les 16 extraits du chapitre en expériences exécutables. "
            "Les exemples 1 à 13, 15 et 16 sont locaux. Seul l'exemple 14 peut appeler OpenAI."
        ),
        markdown(
            "## Objectifs pédagogiques\n\n"
            "À la fin du notebook, vous saurez mesurer un budget de tokens, comparer plusieurs "
            "découpages, préserver la structure, enrichir les métadonnées et évaluer les réglages."
        ),
        markdown("## 0. Préparer Colab ou Jupyter\n\nCette cellule installe uniquement les outils de chunking."),
        code(CHAPTER_3_BOOTSTRAP),
        markdown(
            "## Document fil rouge\n\n"
            "Chaque script contient son propre petit jeu de données afin de pouvoir aussi être lancé séparément."
        ),
    ]
    for index, (filename, title, explanation) in enumerate(lessons, start=1):
        if filename == "14_contextual_retrieval.py":
            cells.extend(
                [
                    markdown(
                        "## Configuration facultative pour OpenAI\n\n"
                        "Laissez la case décochée si vous n'avez pas de clé : cela ne bloque aucun autre exemple."
                    ),
                    code(CHAPTER_3_OPENAI),
                ]
            )
        source = (examples / filename).read_text(encoding="utf-8")
        cells.extend(
            [
                markdown(
                    f"## {index}. {title}\n\n{explanation}\n\n"
                    f"Script correspondant : [`{filename}`](examples/{filename})"
                ),
                code("# ruff: noqa: F811\n" + source),
            ]
        )
    cells.append(
        markdown(
            "## Bilan\n\n"
            "Il n'existe pas de taille universelle. Mesurez les tokens, conservez les métadonnées "
            "de position, puis comparez les stratégies sur des questions représentatives de votre corpus."
        )
    )
    return notebook(cells)


CHAPTER_4_BOOTSTRAP = f'''import os
import subprocess
import sys
from pathlib import Path

if not Path("src").is_dir():
    if not Path("rag-en-pratique").is_dir():
        subprocess.run(["git", "clone", "{REPOSITORY_URL}.git"], check=True)
    os.chdir("rag-en-pratique")

subprocess.run(
    [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "-e",
        ".[retrieval,huggingface]",
    ],
    check=True,
)
print("Environnement du chapitre 4 prêt :", Path.cwd())
'''

CHAPTER_4_OPENAI = '''# @title Activer les exemples OpenAI 1, 2, 3 et 9
UTILISER_OPENAI = False # @param {type:"boolean"}

if UTILISER_OPENAI:
    import os
    import subprocess
    import sys
    from getpass import getpass

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-e", ".[openai]"],
        check=True,
    )
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass("OPENAI_API_KEY : ")
    if not os.getenv("OPENAI_MODEL"):
        os.environ["OPENAI_MODEL"] = input("OPENAI_MODEL : ").strip()
    print("OpenAI est activé pour ce notebook.")
else:
    print("OpenAI désactivé. Les algorithmes locaux restent exécutables.")
'''


def chapter_4() -> dict[str, object]:
    badge = (
        "https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/"
        "blob/main/chapters/chapitre-04-retrieval-avance/04_retrieval_avance.ipynb"
    )
    examples = ROOT / "chapters/chapitre-04-retrieval-avance/examples"
    lessons = [
        ("01_query_rewriting.py", "Query Rewriting", "Rendre une question conversationnelle autonome avec OpenAI."),
        ("02_query_expansion.py", "Query Expansion et RRF", "Diversifier les formulations, puis fusionner les classements."),
        ("03_hyde.py", "HyDE", "Générer un document hypothétique OpenAI avant la recherche."),
        ("04_hybrid_search.py", "Recherche hybride", "Combiner un signal dense pédagogique et BM25."),
        ("05_reranking.py", "Re-ranking", "Reclasser les candidats avec un CrossEncoder Hugging Face."),
        ("06_mmr_pseudocode.py", "MMR pas à pas", "Équilibrer pertinence et diversité avec une formule explicite."),
        ("07_mmr.py", "MMR dans un vector store", "Comprendre le contrat d'une recherche MMR intégrée."),
        ("08_reorder.py", "Réorganisation en V", "Placer les meilleurs passages aux extrémités du prompt."),
        ("09_compression.py", "Compression contextuelle", "Extraire avec OpenAI les phrases utiles de chaque passage."),
        ("10_pipeline_ordre.py", "Pipeline complet", "Assembler les étapes dans un ordre observable et testable."),
    ]
    cells = [
        markdown(
            f"# Chapitre 4 — Retrieval avancé\n\n"
            f"[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge})\n\n"
            "Ce notebook contient les 10 exemples du chapitre. OpenAI est facultatif ; "
            "BM25, RRF, MMR et le réordonnancement fonctionnent sans clé."
        ),
        markdown(
            "## Ressources utiles\n\n"
            "- [OpenAI Responses API](https://developers.openai.com/api/docs/guides/text)\n"
            "- [Sentence Transformers — Retrieve & Re-Rank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)\n"
            "- [rank-bm25](https://github.com/dorianbrown/rank_bm25)"
        ),
        markdown("## 0. Préparer Colab ou Jupyter\n\nInstallation de BM25 et Sentence Transformers."),
        code(CHAPTER_4_BOOTSTRAP),
        markdown(
            "## Configuration OpenAI facultative\n\n"
            "Activez cette cellule uniquement pour exécuter les exemples 1, 2, 3 et 9."
        ),
        code(CHAPTER_4_OPENAI),
    ]
    for index, (filename, title, explanation) in enumerate(lessons, start=1):
        source = (examples / filename).read_text(encoding="utf-8")
        cells.extend(
            [
                markdown(
                    f"## {index}. {title}\n\n{explanation}\n\n"
                    f"Script correspondant : [`{filename}`](examples/{filename})"
                ),
                code("# ruff: noqa: F811\n" + source),
            ]
        )
    cells.append(
        markdown(
            "## Bilan\n\n"
            "Un retrieval avancé est une cascade : réparer la requête, élargir le rappel, "
            "fusionner, reclasser, diversifier, compresser puis ordonner le contexte. "
            "Chaque étape doit être évaluée séparément avant d'être conservée."
        )
    )
    return notebook(cells)


def chapter_2() -> dict[str, object]:
    badge = (
        "https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/"
        "blob/main/chapters/chapitre-02-premier-rag/02_premier_rag.ipynb"
    )
    return notebook(
        [
            markdown(
                f"# Chapitre 2 — Construire un premier RAG\n\n"
                f"[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge})\n\n"
                "Ce notebook met en œuvre ingestion, chunking, embeddings, retrieval, "
                "génération et citations avec OpenAI, Hugging Face ou Ollama."
            ),
            markdown(
                "## Scripts du chapitre\n\n"
                "1. [`01_document_loading.py`](examples/01_document_loading.py)\n"
                "2. [`02_pipeline_ingestion.py`](examples/02_pipeline_ingestion.py)\n"
                "3. [`03_generator_rag.py`](examples/03_generator_rag.py)\n"
                "4. [`04_naive_rag_complet.py`](examples/04_naive_rag_complet.py)"
            ),
            markdown(
                "## 1. Choisir un fournisseur\n\n"
                "OpenAI et Hugging Face fonctionnent dans Colab. Ollama est prévu pour un "
                "notebook local relié à un serveur Ollama déjà démarré."
            ),
            code(PROVIDER_SELECTION),
            markdown("## 2. Préparer le dépôt\n\nLa cellule fonctionne dans Colab et depuis la racine du dépôt."),
            code(BOOTSTRAP),
            markdown(
                "## 3. Configurer le fournisseur\n\n"
                "En mode OpenAI, la clé est saisie de manière masquée et n'est jamais enregistrée. "
                "Hugging Face télécharge les modèles publics au premier lancement."
            ),
            code(PROVIDER_SETUP),
            markdown(
                "## 4. Charger les documents\n\n"
                "Correspond à [`01_document_loading.py`](examples/01_document_loading.py)."
            ),
            code(
                '''from pathlib import Path

from rag_en_pratique.core import Document

data_directory = Path("data/sample")
documents = [
    Document(path.read_text(encoding="utf-8"), {"source": path.name})
    for path in sorted(data_directory.glob("*.md"))
    if path.name.lower() != "readme.md"
]
[(doc.metadata["source"], len(doc.text)) for doc in documents]
'''
            ),
            markdown("## 5. Découper les documents"),
            code(
                '''from rag_en_pratique.core import split_documents

chunks = split_documents(documents, chunk_size=60, overlap=10)
print(f"{len(documents)} documents -> {len(chunks)} chunks")
chunks[0]
'''
            ),
            markdown(
                "## 6. Indexer et rechercher\n\n"
                "Correspond à [`02_pipeline_ingestion.py`](examples/02_pipeline_ingestion.py)."
            ),
            code(
                '''from rag_en_pratique.core import InMemoryVectorStore
from rag_en_pratique.providers import create_embedder

store = InMemoryVectorStore(create_embedder(PROVIDER))
store.add(chunks)
results = store.search("Quel est le délai pour retourner un produit ?", top_k=3)
[(round(item.score, 3), item.document.metadata["source"]) for item in results]
'''
            ),
            markdown(
                "## 7. Générer la réponse\n\n"
                "Correspond à [`03_generator_rag.py`](examples/03_generator_rag.py) et "
                "[`04_naive_rag_complet.py`](examples/04_naive_rag_complet.py)."
            ),
            code(
                '''from rag_en_pratique.core import RAGPipeline
from rag_en_pratique.providers import create_generator

rag = RAGPipeline(store, create_generator(PROVIDER))
response = rag.ask("Sous combien de jours peut-on retourner un produit ?")
print(response["answer"])
'''
            ),
            markdown("## 8. Examiner les sources\n\nUne application RAG doit rendre ses sources inspectables."),
            code(
                '''for source in response["sources"]:
    print(source["score"], source["metadata"]["source"])
    print(source["text"][:250])
    print()
'''
            ),
            markdown(
                "## Pour aller plus loin\n\n"
                "Comparez plusieurs tailles de chunks, modifiez `top_k`, ajoutez un document "
                "et vérifiez que la réponse cite toujours la bonne source."
            ),
        ]
    )


def chapter_9() -> dict[str, object]:
    badge = (
        "https://colab.research.google.com/github/Ahouahounko/rag-en-pratique/"
        "blob/main/chapters/chapitre-09-docurag/09_docurag.ipynb"
    )
    return notebook(
        [
            markdown(
                f"# Chapitre 9 — DocuRAG\n\n"
                f"[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge})\n\n"
                "DocuRAG organise le pipeline du chapitre 2 en application modulaire "
                "compatible avec OpenAI, Hugging Face et Ollama."
            ),
            markdown(
                "## Scripts et fichiers du chapitre\n\n"
                "1. [`01_arborescence.txt`](examples/01_arborescence.txt)\n"
                "2. [`02_config.py`](examples/02_config.py)\n"
                "3. [`03_env_example.txt`](examples/03_env_example.txt)\n"
                "4. [`04_requirements.txt`](examples/04_requirements.txt)\n"
                "5. [`05_loader.py`](examples/05_loader.py)\n"
                "6. [`06_chunker.py`](examples/06_chunker.py)\n"
                "7. [`07_indexer.py`](examples/07_indexer.py)\n"
                "8. [`08_pipeline_ingestion.py`](examples/08_pipeline_ingestion.py)\n"
                "9. [`09_retriever.py`](examples/09_retriever.py)\n"
                "10. [`10_prompts.py`](examples/10_prompts.py)\n"
                "11. [`11_generator.py`](examples/11_generator.py)\n"
                "12. [`12_schemas.py`](examples/12_schemas.py)\n"
                "13. [`13_api_main.py`](examples/13_api_main.py)\n"
                "14. [`14_interface.py`](examples/14_interface.py)\n"
                "15. [`15_test_evaluation.py`](examples/15_test_evaluation.py)\n"
                "16. [`16_dockerfile.txt`](examples/16_dockerfile.txt)\n"
                "17. [`17_compose.yml`](examples/17_compose.yml)\n"
                "18. [`18_demarrage.sh`](examples/18_demarrage.sh)"
            ),
            markdown(
                "## 1. Choisir un fournisseur\n\n"
                "OpenAI et Hugging Face fonctionnent dans Colab. Ollama est destiné à "
                "l'exécution locale, avec le serveur démarré avant le notebook."
            ),
            code(PROVIDER_SELECTION),
            markdown("## 2. Préparer le dépôt"),
            code(BOOTSTRAP),
            markdown("## 3. Configurer le fournisseur"),
            code(PROVIDER_SETUP),
            markdown(
                "## 4. Charger l'application DocuRAG\n\n"
                "Configuration, chargement et chunking correspondent aux exemples 02 à 06."
            ),
            code(
                '''import sys
from pathlib import Path

runnable = Path("chapters/chapitre-09-docurag/runnable").resolve()
sys.path.insert(0, str(runnable))

from docurag import DocuRAG
from docurag.config import Settings

settings = Settings.from_env()
app = DocuRAG(settings)
'''
            ),
            markdown(
                "## 5. Ingérer et indexer un dossier\n\n"
                "Correspond aux exemples 07 et 08. Le fournisseur choisi calcule les embeddings."
            ),
            code(
                '''chunk_count = app.ingest(Path("data/sample"))
print(f"{chunk_count} chunks indexés")
'''
            ),
            markdown(
                "## 6. Interroger DocuRAG\n\n"
                "Correspond aux exemples 09 à 13 : retrieval, prompts, génération, schémas et API."
            ),
            code(
                '''result = app.ask("Quel est le délai de livraison standard ?")
print(result["answer"])
'''
            ),
            markdown("## 7. Inspecter la traçabilité"),
            code(
                '''for rank, source in enumerate(result["sources"], start=1):
    print(f"#{rank} score={source['score']} source={source['metadata']['source']}")
    print(source["text"][:300])
    print()
'''
            ),
            markdown("## 8. Tester une question absente des documents"),
            code(
                '''unknown = app.ask("Quel est le numéro de téléphone du directeur ?")
print(unknown["answer"])
'''
            ),
            markdown(
                "## 9. Interface, évaluation et déploiement\n\n"
                "Les exemples 14 à 18 couvrent Streamlit, l'évaluation, Docker, "
                "Compose et le démarrage.\n\n"
                "## Architecture\n\n"
                "- `config.py` : configuration explicite ;\n"
                "- `loaders.py` : chargement Markdown, texte et PDF facultatif ;\n"
                "- `pipeline.py` : ingestion, retrieval et génération ;\n"
                "- `cli.py` : interface en ligne de commande ;\n"
                "- `rag_en_pratique.core` : composants partagés et testables."
            ),
        ]
    )


def write(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))


def main() -> None:
    write(ROOT / "chapters/chapitre-02-premier-rag/02_premier_rag.ipynb", chapter_2())
    write(
        ROOT / "chapters/chapitre-03-donnees-et-chunking/03_donnees_et_chunking.ipynb",
        chapter_3(),
    )
    write(
        ROOT / "chapters/chapitre-04-retrieval-avance/04_retrieval_avance.ipynb",
        chapter_4(),
    )
    write(ROOT / "chapters/chapitre-09-docurag/09_docurag.ipynb", chapter_9())


if __name__ == "__main__":
    main()
