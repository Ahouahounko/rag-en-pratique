"""Formater les passages avec des balises et des métadonnées explicites."""

from __future__ import annotations

from html import escape

from rag_en_pratique.prompting import Passage

SYSTEME_BALISE = """Tes réponses s'appuient exclusivement sur les extraits contenus dans <extraits>.
Pour citer, utilise l'attribut id : [doc_2].
Le champ <date_revision> fait autorité en cas de contradiction : le plus récent prévaut."""


def formater_balise(passages: list[Passage]) -> str:
    lignes = ["<extraits>"]
    for numero, passage in enumerate(passages, start=1):
        meta = passage.metadata
        lignes.extend(
            [
                f'  <extrait id="doc_{numero}">',
                f"    <source>{escape(str(meta.get('source', 'inconnu')))}</source>",
                f"    <page>{escape(str(meta.get('page', '?')))}</page>",
                f"    <date_revision>{escape(str(meta.get('date', 'non précisée')))}</date_revision>",
                f"    <service>{escape(str(meta.get('departement', 'non précisé')))}</service>",
                f"    <contenu>{escape(passage.page_content)}</contenu>",
                "  </extrait>",
            ]
        )
    lignes.append("</extraits>")
    return "\n".join(lignes)


if __name__ == "__main__":
    exemple = Passage("Remboursement < 30 jours.", {"source": "cgv.pdf", "date": "2026-01-01"})
    print(formater_balise([exemple]))
