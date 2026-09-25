import re
from dataclasses import dataclass

@dataclass
class SectionDocument:
    """Une zone thematiquement coherente : la future cloison etanche."""
    titre: str
    contenu: str
    chemin: str        # Ex. : "Introduction > Analyse > Risques"
    debut_char: int
    fin_char: int


def cartographier_markdown(texte: str) -> list[SectionDocument]:
    """
    Reconstruit l'arborescence d'un document Markdown a partir
    de ses titres. Le chemin hierarchique complet est conserve :
    c'est lui qui servira de contexte a la phase 3.
    """
    motif_titre = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    occurrences = list(motif_titre.finditer(texte))

    sections, pile = [], []      # pile = chemin hierarchique courant

    for i, occ in enumerate(occurrences):
        niveau = len(occ.group(1))
        titre  = occ.group(2).strip()

        # On tronque la pile au niveau du titre courant, puis on empile
        pile = pile[: niveau - 1]
        pile.append(titre)

        debut = occ.end()
        fin   = occurrences[i + 1].start() if i + 1 < len(occurrences) else len(texte)

        sections.append(SectionDocument(
            titre      = titre,
            contenu    = texte[debut:fin].strip(),
            chemin     = " > ".join(pile),
            debut_char = debut,
            fin_char   = fin,
        ))

    return sections
