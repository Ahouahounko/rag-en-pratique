"""Interface en ligne de commande de DocuRAG."""

from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import DocuRAG


def main() -> None:
    parser = argparse.ArgumentParser(description="Interroger un dossier avec DocuRAG")
    parser.add_argument("documents", type=Path)
    parser.add_argument("question")
    args = parser.parse_args()
    app = DocuRAG()
    count = app.ingest(args.documents)
    result = app.ask(args.question)
    print(f"{count} chunk(s) indexé(s)\n")
    print(result["answer"])


if __name__ == "__main__":
    main()
