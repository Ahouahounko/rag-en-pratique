"""Lance les exemples purement locaux du chapitre 6."""

from __future__ import annotations

import runpy
from pathlib import Path

EXEMPLES_LOCAUX = [
    "02_format_simple.py",
    "03_format_balise.py",
    "04_format_annote.py",
    "05_verif_citations.py",
    "06_budget_tokens.py",
    "16_injection.py",
    "17_regression_prompts.py",
]


def main() -> None:
    examples = Path(__file__).parents[1] / "examples"
    for filename in EXEMPLES_LOCAUX:
        print(f"\n{'=' * 12} {filename} {'=' * 12}")
        runpy.run_path(str(examples / filename), run_name="__main__")
    print("\nLes exemples OpenAI n'ont pas été appelés.")


if __name__ == "__main__":
    main()
