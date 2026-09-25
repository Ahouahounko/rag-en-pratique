"""Lance les exemples du chapitre 8 sans effectuer d'appel OpenAI."""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    examples = Path(__file__).parents[1] / "examples"
    for path in sorted(examples.glob("[0-9][0-9]_*.py")):
        print(f"\n{'=' * 12} {path.name} {'=' * 12}")
        runpy.run_path(str(path), run_name="__main__")
    print("\nAucun appel OpenAI n'a été effectué.")


if __name__ == "__main__":
    main()
