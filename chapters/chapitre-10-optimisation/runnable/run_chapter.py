"""Exécute les six exemples du chapitre 10 sans appel distant."""

from __future__ import annotations

import runpy
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def main() -> None:
    for path in sorted(EXAMPLES.glob("[0-9][0-9]_*.py")):
        print(f"\n{'=' * 12} {path.name} {'=' * 12}")
        runpy.run_path(str(path), run_name="__main__")
    print("\nAucun appel OpenAI ou Hugging Face n'a été effectué.")


if __name__ == "__main__":
    main()
