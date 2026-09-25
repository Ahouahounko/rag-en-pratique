"""Produire une analyse documentaire structurée sans exposer un raisonnement caché."""

from __future__ import annotations

from rag_en_pratique.prompting import generer, openai_configure

INSTRUCTIONS = """Tu es un analyste documentaire. Appuie-toi exclusivement sur les extraits.
Structure la sortie en quatre sections :
<apports>faits utiles de chaque extrait avec citations</apports>
<conclusion>conclusion étayée, sans raisonnement privé</conclusion>
<reponse>réponse finale en trois phrases maximum</reponse>
<limites>informations que les extraits ne permettent pas d'établir</limites>"""


def analyser(contexte: str, question: str, *, client=None, model: str | None = None) -> str:
    return generer(
        INSTRUCTIONS,
        f"EXTRAITS :\n{contexte}\n\nQUESTION : {question}",
        client=client,
        model=model,
    )


if __name__ == "__main__":
    if openai_configure():
        print(analyser("[doc_1] Garantie de 24 mois.", "Quelle garantie ?"))
    else:
        print(INSTRUCTIONS)
