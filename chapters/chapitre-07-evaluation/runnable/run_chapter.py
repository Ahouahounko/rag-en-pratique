"""Lance les quatre exemples du chapitre 7 sans appel API."""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    examples = Path(__file__).parents[1] / "examples"
    for path in sorted(examples.glob("[0-9][0-9]_*.py")):
        print(f"\n{'=' * 12} {path.name} {'=' * 12}")
        runpy.run_path(str(path), run_name="__main__")
    print("\nAucun juge OpenAI n'a été appelé.")


if __name__ == "__main__":
    main()
