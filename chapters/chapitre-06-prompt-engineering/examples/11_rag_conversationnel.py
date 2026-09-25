"""RAG conversationnel avec condensation et historique explicitement borné."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from rag_en_pratique.prompting import formater_simple, generer, openai_configure


@dataclass
class RAGConversationnel:
    retriever: object
    client: object | None = None
    model: str | None = None
    max_tours: int = 4
    historique: deque[tuple[str, str]] = field(default_factory=deque)

    def question_autonome(self, question: str) -> str:
        if not self.historique:
            return question
        histoire = "\n".join(f"U: {q}\nA: {r}" for q, r in self.historique)
        return generer(
            "Reformule la question en question autonome. Ne réponds pas.",
            f"HISTORIQUE :\n{histoire}\n\nQUESTION : {question}",
            client=self.client,
            model=self.model,
        )

    def demander(self, question: str) -> dict[str, object]:
        autonome = self.question_autonome(question)
        passages = list(self.retriever.invoke(autonome))
        reponse = generer(
            "Réponds uniquement avec les extraits. Cite chaque affirmation avec [doc_N].",
            f"EXTRAITS :\n{formater_simple(passages)}\n\nQUESTION : {autonome}",
            client=self.client,
            model=self.model,
        )
        self.historique.append((question, reponse))
        while len(self.historique) > self.max_tours:
            self.historique.popleft()
        return {"reponse": reponse, "question_autonome": autonome, "sources": passages}


if __name__ == "__main__" and not openai_configure():
    print("Exemple prêt : configurez OPENAI_API_KEY et OPENAI_MODEL.")
