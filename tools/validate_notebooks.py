"""Valide et, sur demande, exécute les cellules Python des notebooks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(path: Path, *, execute: bool) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    namespace: dict[str, object] = {}
    for index, cell in enumerate(payload["cells"], start=1):
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        compiled = compile(source, f"{path}:cell-{index}", "exec")
        if execute:
            exec(compiled, namespace)
    print(f"{path}: OK")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    for path in args.paths:
        validate(path, execute=args.execute)


if __name__ == "__main__":
    main()
