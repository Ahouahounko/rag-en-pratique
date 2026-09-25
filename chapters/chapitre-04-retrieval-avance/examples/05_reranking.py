"""Re-ranking des candidats avec un CrossEncoder Hugging Face."""

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class Passage:
    page_content: str
    source: str


class Retriever(Protocol):
    def invoke(self, question: str) -> list[Passage]: ...


def charger_reranker() -> Any:
    from sentence_transformers import CrossEncoder

    return CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")


def rechercher_et_reclasser(
    question: str,
    retriever: Retriever,
    *,
    reranker: Any = None,
    n_candidats: int = 20,
    n_final: int = 5,
) -> list[Passage]:
    candidats = retriever.invoke(question)[:n_candidats]
    if not candidats:
        return []
    modele = reranker or charger_reranker()
    scores = modele.predict([(question, doc.page_content) for doc in candidats])
    classes = sorted(zip(candidats, scores, strict=True), key=lambda paire: paire[1], reverse=True)
    return [document for document, _ in classes[:n_final]]


class RetrieverExemple:
    def invoke(self, question: str) -> list[Passage]:
        del question
        return [
            Passage("La livraison prend cinq jours.", "livraison.md"),
            Passage("Les retours sont acceptés sous trente jours.", "retours.md"),
        ]


if __name__ == "__main__":
    for passage in rechercher_et_reclasser("Quel est le délai de retour ?", RetrieverExemple()):
        print(passage.source, passage.page_content)
