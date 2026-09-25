"""Utiliser MMR via l'interface d'un vector store."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Passage:
    page_content: str
    source: str


def selection_diversifiee(
    base_vectorielle,
    question: str,
    k: int = 5,
    fetch_k: int = 25,
    lambda_mult: float = 0.6,
) -> list[Passage]:
    """Délègue au vector store la sélection pertinente et complémentaire."""

    return base_vectorielle.max_marginal_relevance_search(
        query=question,
        k=k,
        fetch_k=fetch_k,
        lambda_mult=lambda_mult,
    )


class VectorStoreExemple:
    """Double pédagogique qui montre le contrat attendu du vector store."""

    def __init__(self, documents: list[Passage]) -> None:
        self.documents = documents

    def max_marginal_relevance_search(
        self,
        *,
        query: str,
        k: int,
        fetch_k: int,
        lambda_mult: float,
    ) -> list[Passage]:
        del query, fetch_k, lambda_mult
        return self.documents[:k]


if __name__ == "__main__":
    store = VectorStoreExemple(
        [
            Passage("Politique de retour", "retours.md"),
            Passage("Délai de remboursement", "remboursement.md"),
        ]
    )
    print(selection_diversifiee(store, "retour et remboursement", k=2))
