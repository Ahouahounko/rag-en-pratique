# src/generation/generator.py
import logging
from dataclasses import dataclass, field
from typing import Iterator

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import get_settings
from src.generation.prompts import SYSTEME, UTILISATEUR, VERSION_PROMPT
from src.retrieval.retriever import Passage

logger = logging.getLogger(__name__)

ABSTENTION = "Cette information ne figure pas dans les documents consultes."


@dataclass
class Reponse:
    texte: str
    sources: list[dict] = field(default_factory=list)
    confiance: str = "Bas"          # "Haut" / "Moyen" / "Bas"
    nb_passages: int = 0
    version_prompt: str = VERSION_PROMPT


class Generateur:
    """Genere une reponse ancree, citee et assortie d'un niveau
    de confiance."""

    def __init__(self):
        config = get_settings()
        self.nom = config.app_name

        self.modele = ChatOpenAI(
            model=config.llm_model,
            temperature=config.llm_temperature,   # 0 : reproductible
            max_tokens=config.llm_max_tokens,
            streaming=True,
        )

        gabarit = ChatPromptTemplate.from_messages([
            ("system", SYSTEME),
            ("human", UTILISATEUR),
        ])
        self.chaine = gabarit | self.modele | StrOutputParser()

    def formater(self, passages: list[Passage]) -> str:
        """Assemble les passages : identifiant stable + separateur.

        L'identifiant doc_N est genere ICI et devra correspondre a
        l'ordre des sources renvoyees, sinon les citations du
        modele pointeront vers le mauvais document.
        """
        blocs = []
        for numero, passage in enumerate(passages, start=1):
            entete = f"[doc_{numero}] {passage.source}"
            if passage.page:
                entete += f", page {passage.page}"
            blocs.append(f"{entete}\n{passage.texte}")
        return "\n\n---\n\n".join(blocs)

    def _confiance(self, passages: list[Passage]) -> str:
        """Indicateur qualitatif, PAS une probabilite.

        Il sert a inviter l'utilisateur a verifier quand le
        systeme est peu sur. Trois niveaux suffisent : une valeur
        decimale suggererait une precision qui n'existe pas.
        """
        if not passages:
            return "Bas"
        meilleur = max(p.score_rerank if p.score_rerank else p.score_dense
                       for p in passages)
        if meilleur >= 0.7:
            return "Haut"
        return "Moyen" if meilleur >= 0.4 else "Bas"

    def _sources(self, passages: list[Passage]) -> list[dict]:
        """Sources uniques, dans l'ordre des identifiants doc_N."""
        sources, vues = [], set()
        for passage in passages:
            cle = (passage.source, passage.page)
            if cle in vues:
                continue
            vues.add(cle)
            sources.append({
                "document": passage.source,
                "page": passage.page,
                "departement": passage.departement,
                "pertinence": round(
                    passage.score_rerank or passage.score_dense, 3),
            })
        return sources

    def repondre(self, question: str,
                 passages: list[Passage]) -> Reponse:
        """Reponse complete. Sans passage, on s'abstient sans
        meme appeler le modele : economie et surete."""
        if not passages:
            return Reponse(texte=ABSTENTION, confiance="Bas")

        texte = self.chaine.invoke({
            "app_name": self.nom,
            "contexte": self.formater(passages),
            "question": question,
        })

        return Reponse(
            texte=texte,
            sources=self._sources(passages),
            confiance=self._confiance(passages),
            nb_passages=len(passages),
        )

    def diffuser(self, question: str,
                 passages: list[Passage]) -> Iterator[str]:
        """Version en flux : les jetons arrivent au fil de l'eau."""
        if not passages:
            yield ABSTENTION
            return

        yield from self.chaine.stream({
            "app_name": self.nom,
            "contexte": self.formater(passages),
            "question": question,
        })
