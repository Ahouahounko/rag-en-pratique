import re

def clean_document(text: str) -> str:
    """
    Nettoie un document brut avant le chunking.

    Bonne pratique : appliquer ce nettoyage AVANT le chunking,
    jamais apres. Le bruit retire ici ne polluera pas les embeddings.
    """
    # Normaliser les sauts de ligne (Windows/Unix/Mac)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Supprimer les numeros de page isoles (lignes ne contenant qu'un nombre)
    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

    # Reduire les espaces multiples en un seul
    text = re.sub(r"[ \t]+", " ", text)

    # Reduire les sauts de ligne multiples (max 2 = separation paragraphe)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Supprimer les caracteres de controle (sauf \n et \t)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)

    # Supprimer les espaces en debut et fin de chaque ligne
    text = "\n".join(line.strip() for line in text.split("\n"))

    return text.strip()
