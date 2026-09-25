import runpy
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "chapters/chapitre-03-donnees-et-chunking/examples"


def load(filename: str) -> dict[str, object]:
    return runpy.run_path(str(EXAMPLES / filename))


def test_recursive_and_fixed_chunking_are_executable() -> None:
    recursive = load("05_mecanisme_recursif.py")
    chunks = recursive["decouper_recursivement"]("alpha beta gamma delta", [" ", ""], 10)
    assert "".join(chunks).replace(" ", "") == "alphabetagammadelta"

    fixed = load("04_chunking_fixe.py")
    fixed_chunks = fixed["decoupage_fixe"]("Le RAG découpe un document.", 5, 1)
    assert len(fixed_chunks) >= 2


def test_structure_and_metadata_examples() -> None:
    mapping = load("07_cartographie.py")
    sections = mapping["cartographier_markdown"]("# A\nTexte\n## B\nSuite")
    assert [section.chemin for section in sections] == ["A", "A > B"]

    ast_chunking = load("09_chunking_ast.py")
    chunks = ast_chunking["decouper_code_python"]("import os\n\ndef f():\n    return os.name", "x.py")
    assert chunks[0]["metadonnees"]["symbole"] == "f"


def test_semantic_and_late_chunking_shapes() -> None:
    semantic = load("11_chunking_semantique.py")
    chunks = semantic["chunking_semantique"](
        "Les retours sont possibles. Le remboursement suit. La livraison arrive demain.",
        semantic["ModeleTFIDF"](),
        50,
    )
    assert len(chunks) >= 2

    late = load("15_late_chunking.py")
    model = late["ModeleLongContextePedagogique"](dimension=4)
    boundaries = late["frontieres_en_tokens"]("Un petit document de test.", 12, model.tokenizer)
    vectors = late["late_chunking"]("Un petit document de test.", model, boundaries)
    assert all(isinstance(vector, np.ndarray) and vector.shape == (4,) for vector in vectors)


def test_grid_search_returns_comparable_results() -> None:
    grid = load("16_grid_search.py")
    results = grid["explorer"](
        ["Retours\n\nLe retour dure trente jours."],
        [("Quel délai de retour ?", "trente")],
    )
    assert len(results) == len(grid["TAILLES"]) * len(grid["OVERLAPS"]) * len(grid["STRATEGIES"])
    assert all("precision_contextuelle" in result for result in results)
