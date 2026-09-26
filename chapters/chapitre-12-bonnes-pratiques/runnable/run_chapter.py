"""Exécute les démonstrations locales du chapitre 12."""

from __future__ import annotations

import runpy
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def main() -> None:
    for path in sorted(EXAMPLES.glob("[0-9][0-9]_*")):
        print(f"\n{'=' * 12} {path.name} {'=' * 12}")
        if path.suffix == ".py":
            runpy.run_path(str(path), run_name="__main__")
        else:
            print(path.read_text(encoding="utf-8"))
    print("\nAucun appel distant n'a été effectué.")


if __name__ == "__main__":
    main()
