"""Point d'entrée portable pour DocuRAG."""

from __future__ import annotations

import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
sys.path.insert(0, str(REPOSITORY / "src"))
sys.path.insert(0, str(HERE))

from docurag.cli import main  # noqa: E402


if __name__ == "__main__":
    main()
