import hashlib
from dataclasses import dataclass, field

from scipy import stats


def assigner_variante(identifiant_utilisateur: str,
                      graine: str = "test-embedding-v2") -> str:
    """Assigne A ou B de facon stable et deterministe.

    Le hachage inclut une graine PROPRE A CHAQUE TEST : deux tests
    lances la meme semaine ne doivent jamais correler leurs
    assignations, sinon les biais individuels s'accumulent d'un
    test a l'autre au lieu de s'annuler.
    """
    cle = f"{graine}:{identifiant_utilisateur}".encode()
    empreinte = hashlib.sha256(cle).hexdigest()
    # Le premier caractere hexadecimal suffit : 8 valeurs possibles,
    # reparties uniformement entre A (0-7) et B (8-f).
    return "A" if int(empreinte[0], 16) < 8 else "B"


@dataclass
class ResultatsTest:
    scores_a: list[float] = field(default_factory=list)
    scores_b: list[float] = field(default_factory=list)

    def effectif_atteint(self, effectif_requis: int) -> bool:
        return (len(self.scores_a) >= effectif_requis
                and len(self.scores_b) >= effectif_requis)

    def analyser(self) -> dict:
        """N'appeler qu'une fois l'effectif requis atteint (cf. warning)."""
        t_stat, p_valeur = stats.ttest_ind(self.scores_a, self.scores_b)
        return {
            "moyenne_a": sum(self.scores_a) / len(self.scores_a),
            "moyenne_b": sum(self.scores_b) / len(self.scores_b),
            "p_valeur": p_valeur,
            "significatif": p_valeur < 0.05,
        }
