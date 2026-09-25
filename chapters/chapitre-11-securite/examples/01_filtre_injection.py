import logging
import re

logger = logging.getLogger(__name__)

# Marqueurs d'une tentative d'injection. Volontairement courts :
# cette liste attrape le grossier, pas le sophistique.
MOTIFS = [
    r"ignore[sz]?\s+(toutes?\s+)?(les\s+)?instructions",
    r"oublie[sz]?\s+(tout\s+)?ce\s+qui\s+prec.de",
    r"nouvelles?\s+instructions?\s+syst.me",
    r"instructions?\s+prioritaires?",
    r"tu\s+es\s+(desormais|maintenant)\s+(?!un\s+assistant)",
    r"ne\s+mentionne\s+jamais",
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"(system|assistant)\s*:\s*",
    r"<\s*/?\s*system\s*>",
    r"\[INST\]",
]


def analyser(texte: str) -> tuple[bool, list[str]]:
    """Cherche des marqueurs d'injection dans un document."""
    trouves = [motif for motif in MOTIFS
               if re.search(motif, texte, re.IGNORECASE)]
    return bool(trouves), trouves


def ingerer_si_sain(texte: str, source: str,
                    mettre_en_quarantaine=None) -> bool:
    """Autorise l'indexation, ou place le document en quarantaine.

    On NE SUPPRIME PAS le document suspect : on l'ecarte de
    l'index et on le signale. Un faux positif doit pouvoir etre
    revu par un humain, sinon l'equipe finira par desactiver le
    filtre pour cause de trop-plein d'alertes.
    """
    suspect, motifs = analyser(texte)

    if suspect:
        logger.warning("Document ecarte : %s | motifs=%s", source, motifs)
        if mettre_en_quarantaine:
            mettre_en_quarantaine(source, motifs)
        return False

    return True
