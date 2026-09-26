"""Harnais de comparaison des configurations de chunking."""

from __future__ import annotations

from collections.abc import Callable, Sequence


def _texte(chunk: object) -> str:
    return str(getattr(chunk, "texte", getattr(chunk, "text", chunk)))


def tester_decoupages(
    documents: Sequence[object],
    questions: Sequence[dict[str, str]],
    configurations: Sequence[dict[str, int]],
    *,
    decouper: Callable[..., list[object]],
    indexer: Callable[[list[object]], object],
    k: int = 5,
) -> list[dict[str, float | int]]:
    if not questions or not configurations:
        raise ValueError("questions et configurations ne peuvent pas être vides")
    if k <= 0:
        raise ValueError("k doit être strictement positif")

    results = []
    for config in configurations:
        chunks = decouper(documents, **config)
        index = indexer(chunks)
        complete = partial = missing = 0
        for case in questions:
            expected = case["reponse_attendue"].casefold().strip()
            if not expected:
                raise ValueError("Chaque réponse attendue doit être non vide")
            retrieved = index.chercher(case["texte"], k=k)
            texts = [_texte(chunk).casefold() for chunk in retrieved]
            if any(expected in text for text in texts):
                complete += 1
            elif expected in " ".join(texts):
                partial += 1
            else:
                missing += 1
        total = len(questions)
        results.append(
            {
                **config,
                "complet": complete / total,
                "partiel": partial / total,
                "manque": missing / total,
                "nb_chunks": len(chunks),
            }
        )
    return sorted(results, key=lambda result: (-result["complet"], result["nb_chunks"]))


if __name__ == "__main__":
    print("Exemple prêt : injectez vos fonctions decouper() et indexer().")
