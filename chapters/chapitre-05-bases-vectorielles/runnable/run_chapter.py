"""Lance les exemples locaux du chapitre 5, sans appeler de service distant."""

from __future__ import annotations

import runpy
from pathlib import Path

EXEMPLES_LOCAUX = [
    "01_faiss_hnsw.py",
    "02_faiss_ivf.py",
    "03_filtrage_metadonnees.py",
    "05_qdrant.py",
    "09_ensemble.py",
    "12_retriever_production.py",
]


def main() -> None:
    examples = Path(__file__).parents[1] / "examples"
    for filename in EXEMPLES_LOCAUX:
        print(f"\n{'=' * 12} {filename} {'=' * 12}")
        runpy.run_path(str(examples / filename), run_name="__main__")
    print("\nLes exemples OpenAI, Chroma et Pinecone sont prêts mais non appelés.")


if __name__ == "__main__":
    main()
