"""Lance les démonstrations locales du chapitre 3 dans l'ordre pédagogique."""

from __future__ import annotations

import runpy
from pathlib import Path

EXEMPLES_LOCAUX = [
    "01_comptage_tokens.py",
    "02_validation_taille.py",
    "03_fusion_overlap.py",
    "04_chunking_fixe.py",
    "05_mecanisme_recursif.py",
    "06_chunking_recursif.py",
    "07_cartographie.py",
    "08_context_prepending.py",
    "09_chunking_ast.py",
    "10_chunking_tableaux.py",
    "11_chunking_semantique.py",
    "12_semantique_accumulation.py",
    "13_parent_child.py",
    "15_late_chunking.py",
    "16_grid_search.py",
]


def main() -> None:
    examples = Path(__file__).parents[1] / "examples"
    for filename in EXEMPLES_LOCAUX:
        print(f"\n{'=' * 12} {filename} {'=' * 12}")
        runpy.run_path(str(examples / filename), run_name="__main__")
    print("\nExemple 14 ignoré : il est facultatif et nécessite OpenAI.")


if __name__ == "__main__":
    main()
