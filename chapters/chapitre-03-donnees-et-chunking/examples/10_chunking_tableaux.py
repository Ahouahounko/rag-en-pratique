"""Découpage d'un tableau Markdown avec Chonkie."""

from chonkie import TableChunker

TABLEAU_MARKDOWN = """
| Client   | Montant | Statut   |
|----------|---------|----------|
| Dupont   | 15000   | Réglé    |
| Martin   | 8200    | En cours |
| Mensah   | 9100    | Réglé    |
| Diallo   | 7300    | En cours |
"""


def decouper_tableau(tableau: str, lignes_par_chunk: int = 2) -> list[str]:
    """Retourne des fragments dont chacun conserve l'en-tête du tableau."""

    chunker = TableChunker(chunk_size=lignes_par_chunk)
    return [chunk.text for chunk in chunker(tableau)]


if __name__ == "__main__":
    for index, chunk in enumerate(decouper_tableau(TABLEAU_MARKDOWN), start=1):
        print(f"--- Fragment {index} ---\n{chunk}")
