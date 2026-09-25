import ast


def decouper_code_python(source: str, chemin: str) -> list[dict]:
    """
    Un chunk = une fonction ou une classe complete,
    prefixee des imports du fichier (contexte de dependance).
    """
    arbre  = ast.parse(source)
    lignes = source.splitlines()

    # 1. Extraire le bloc d'imports : il sera prepende a chaque chunk
    imports = [
        ast.get_source_segment(source, n)
        for n in arbre.body
        if isinstance(n, (ast.Import, ast.ImportFrom))
    ]
    entete_imports = "\n".join(i for i in imports if i)

    # 2. Un chunk par definition de haut niveau
    chunks = []
    for n in arbre.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            corps = "\n".join(lignes[n.lineno - 1 : n.end_lineno])
            chunks.append({
                "texte": f"{entete_imports}\n\n{corps}",
                "metadonnees": {
                    "fichier":     chemin,
                    "symbole":     n.name,
                    "type":        type(n).__name__,
                    "ligne_debut": n.lineno,
                    "ligne_fin":   n.end_lineno,
                    "docstring":   ast.get_docstring(n) or "",
                },
            })

    return chunks


if __name__ == "__main__":
    source = '''import math

def aire_cercle(rayon: float) -> float:
    """Calcule l'aire d'un cercle."""
    return math.pi * rayon ** 2

class Client:
    def __init__(self, nom: str) -> None:
        self.nom = nom
'''
    for chunk in decouper_code_python(source, "geometrie.py"):
        print(chunk["metadonnees"])
        print(chunk["texte"], "\n")
