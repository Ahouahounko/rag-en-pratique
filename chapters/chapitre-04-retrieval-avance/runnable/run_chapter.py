"""Lance les exemples du chapitre 4 sans effectuer d'appel OpenAI."""

from __future__ import annotations

import argparse
import runpy
from pathlib import Path

EXEMPLES_SANS_API = [
    "01_query_rewriting.py",
    "02_query_expansion.py",
    "03_hyde.py",
    "04_hybrid_search.py",
    "06_mmr_pseudocode.py",
    "07_mmr.py",
    "08_reorder.py",
    "09_compression.py",
    "10_pipeline_ordre.py",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Démonstrations du retrieval avancé")
    parser.add_argument(
        "--avec-huggingface",
        action="store_true",
        help="Télécharge et exécute aussi le CrossEncoder de l'exemple 5.",
    )
    args = parser.parse_args()
    examples = Path(__file__).parents[1] / "examples"
    fichiers = list(EXEMPLES_SANS_API)
    if args.avec_huggingface:
        fichiers.insert(4, "05_reranking.py")
    for filename in fichiers:
        print(f"\n{'=' * 12} {filename} {'=' * 12}")
        runpy.run_path(str(examples / filename), run_name="__main__")
    if not args.avec_huggingface:
        print("\nExemple 5 ignoré. Ajoutez --avec-huggingface pour télécharger le modèle public.")


if __name__ == "__main__":
    main()
