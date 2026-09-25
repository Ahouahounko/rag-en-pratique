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


BOOTSTRAP = f'''from pathlib import Path
import os
import subprocess
import sys

if not Path("src").is_dir():
    if not Path("rag-en-pratique").is_dir():
        subprocess.run(["git", "clone", "{REPOSITORY_URL}.git"], check=True)
    os.chdir("rag-en-pratique")

sys.path.insert(0, str(Path("src").resolve()))
print("Dépôt prêt :", Path.cwd())
'''


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
                "génération et citations. Le mode hors ligne est actif par défaut."
            ),
            markdown("## 1. Préparer le dépôt\n\nLa cellule fonctionne dans Colab et depuis la racine du dépôt."),
            code(BOOTSTRAP),
            markdown("## 2. Charger les documents de démonstration"),
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
            markdown("## 3. Découper les documents"),
            code(
                '''from rag_en_pratique.core import split_documents

chunks = split_documents(documents, chunk_size=60, overlap=10)
print(f"{len(documents)} documents -> {len(chunks)} chunks")
chunks[0]
'''
            ),
            markdown("## 4. Indexer et rechercher hors ligne"),
            code(
                '''from rag_en_pratique.core import HashingEmbedder, InMemoryVectorStore

store = InMemoryVectorStore(HashingEmbedder(dimensions=256))
store.add(chunks)
results = store.search("Quel est le délai pour retourner un produit ?", top_k=3)
[(round(item.score, 3), item.document.metadata["source"]) for item in results]
'''
            ),
            markdown("## 5. Assembler le pipeline RAG"),
            code(
                '''from rag_en_pratique.core import ExtractiveGenerator, RAGPipeline

rag = RAGPipeline(store, ExtractiveGenerator())
response = rag.ask("Sous combien de jours peut-on retourner un produit ?")
print(response["answer"])
'''
            ),
            markdown("## 6. Examiner les sources\n\nUne application RAG doit rendre ses sources inspectables."),
            code(
                '''for source in response["sources"]:
    print(source["score"], source["metadata"]["source"])
    print(source["text"][:250])
    print()
'''
            ),
            markdown(
                "## 7. Activer OpenAI plus tard (facultatif)\n\n"
                "La cellule ne fait aucun appel tant que `USE_OPENAI` vaut `False`. "
                "Configurez `OPENAI_API_KEY` et `OPENAI_MODEL` dans votre environnement, "
                "sans les inscrire dans le notebook."
            ),
            code(
                '''USE_OPENAI = False

if USE_OPENAI:
    from rag_en_pratique.openai_adapter import OpenAIEmbedder, OpenAIGenerator
    from rag_en_pratique.core import InMemoryVectorStore, RAGPipeline

    online_store = InMemoryVectorStore(OpenAIEmbedder())
    online_store.add(chunks)
    online_rag = RAGPipeline(online_store, OpenAIGenerator())
    online_response = online_rag.ask("Sous combien de jours peut-on retourner un produit ?")
    print(online_response["answer"])
else:
    print("Mode OpenAI désactivé : aucun appel API effectué.")
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
                "DocuRAG organise le pipeline du chapitre 2 en application modulaire. "
                "Le parcours reste entièrement hors ligne par défaut."
            ),
            markdown("## 1. Préparer le dépôt"),
            code(BOOTSTRAP),
            markdown("## 2. Charger l'application DocuRAG"),
            code(
                '''from pathlib import Path
import sys

runnable = Path("chapters/chapitre-09-docurag/runnable").resolve()
sys.path.insert(0, str(runnable))

from docurag import DocuRAG
from docurag.config import Settings

settings = Settings(use_openai=False, chunk_size=60, chunk_overlap=10, top_k=3)
app = DocuRAG(settings)
'''
            ),
            markdown("## 3. Ingérer un dossier"),
            code(
                '''chunk_count = app.ingest(Path("data/sample"))
print(f"{chunk_count} chunks indexés")
'''
            ),
            markdown("## 4. Interroger DocuRAG"),
            code(
                '''result = app.ask("Quel est le délai de livraison standard ?")
print(result["answer"])
'''
            ),
            markdown("## 5. Inspecter la traçabilité"),
            code(
                '''for rank, source in enumerate(result["sources"], start=1):
    print(f"#{rank} score={source['score']} source={source['metadata']['source']}")
    print(source["text"][:300])
    print()
'''
            ),
            markdown("## 6. Tester une question absente des documents"),
            code(
                '''unknown = app.ask("Quel est le numéro de téléphone du directeur ?")
print(unknown["answer"])
'''
            ),
            markdown(
                "## 7. Mode OpenAI facultatif\n\n"
                "Cette cellule reste désactivée. Après configuration de votre clé, "
                "elle remplace les embeddings et la génération hors ligne par les API OpenAI."
            ),
            code(
                '''USE_OPENAI = False

if USE_OPENAI:
    online_settings = Settings.from_env()
    if not online_settings.use_openai:
        raise RuntimeError("Définissez DOCURAG_USE_OPENAI=true")
    online_app = DocuRAG(online_settings)
    online_app.ingest(Path("data/sample"))
    print(online_app.ask("Quel est le délai de livraison standard ?")["answer"])
else:
    print("Mode OpenAI désactivé : aucun appel API effectué.")
'''
            ),
            markdown(
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
    write(ROOT / "chapters/chapitre-09-docurag/09_docurag.ipynb", chapter_9())


if __name__ == "__main__":
    main()
