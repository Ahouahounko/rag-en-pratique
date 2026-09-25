from pathlib import Path


EXPECTED_COUNTS = {
    "chapitre-01-fondations-llm": 0,
    "chapitre-02-premier-rag": 4,
    "chapitre-03-donnees-et-chunking": 16,
    "chapitre-04-retrieval-avance": 10,
    "chapitre-05-bases-vectorielles": 14,
    "chapitre-06-prompt-engineering": 17,
    "chapitre-07-evaluation": 4,
    "chapitre-08-observabilite": 10,
    "chapitre-09-docurag": 18,
    "chapitre-10-optimisation": 6,
    "chapitre-11-securite": 6,
    "chapitre-12-bonnes-pratiques": 6,
}


def test_every_listing_is_extracted() -> None:
    chapters = Path(__file__).parents[1] / "chapters"
    observed = {}
    for chapter, expected in EXPECTED_COUNTS.items():
        examples = chapters / chapter / "examples"
        files = [
            path
            for path in examples.iterdir()
            if path.is_file() and path.name != "README.md"
        ]
        observed[chapter] = len(files)
        assert len(files) == expected
    assert sum(observed.values()) == 111


def test_every_chapter_has_an_examples_manifest() -> None:
    chapters = Path(__file__).parents[1] / "chapters"
    for chapter in EXPECTED_COUNTS:
        assert (chapters / chapter / "examples" / "README.md").is_file()
