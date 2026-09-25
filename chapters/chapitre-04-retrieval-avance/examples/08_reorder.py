"""Réorganisation en V pour limiter l'effet 'lost in the middle'."""

from typing import TypeVar

T = TypeVar("T")


def reordonner_pour_le_prompt(chunks: list[T]) -> list[T]:
    """Place les éléments les mieux classés aux deux extrémités."""

    if len(chunks) <= 2:
        return chunks
    gauche: list[T] = []
    droite: list[T] = []
    for position, chunk in enumerate(chunks):
        (gauche if position % 2 == 0 else droite).append(chunk)
    return gauche + droite[::-1]


if __name__ == "__main__":
    print("Classement initial :", [1, 2, 3, 4, 5, 6])
    print("Ordre dans le prompt :", reordonner_pour_le_prompt([1, 2, 3, 4, 5, 6]))
