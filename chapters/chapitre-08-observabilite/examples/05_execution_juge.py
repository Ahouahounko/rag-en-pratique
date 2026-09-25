import re
from dataclasses import dataclass


@dataclass
class Verdict:
    note: float          # normalisee entre 0 et 1
    note_brute: int      # 1 a 5
    raisonnement: str    # a CONSERVER : c'est votre piste d'audit


def juger(question: str, contexte: str, reponse: str,
          modele_juge) -> Verdict:
    """Note une reponse et conserve la justification.

    Le raisonnement n'est pas decoratif : c'est lui qui vous
    permettra de reperer les jugements aberrants lors de la
    calibration contre des evaluations humaines.
    """
    sortie = modele_juge.invoke(
        PROMPT_JUGE_FAITHFULNESS.format(
            contexte=contexte[:3000],
            question=question,
            reponse=reponse,
        )
    ).content

    trouve = re.search(r"NOTE\s*:\s*([1-5])", sortie, re.IGNORECASE)
    brute = int(trouve.group(1)) if trouve else 3   # 3 = neutre

    explication = re.search(r"RAISONNEMENT\s*:\s*(.+?)(?=NOTE\s*:)",
                            sortie, re.DOTALL | re.IGNORECASE)

    return Verdict(
        note=(brute - 1) / 4,            # 1-5 -> 0-1
        note_brute=brute,
        raisonnement=(explication.group(1).strip()
                      if explication else sortie[:300]),
    )
