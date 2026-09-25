import tiktoken

encoder = tiktoken.get_encoding("cl100k_base")

def compter_tokens(texte: str) -> int:
    """Compte reel des tokens vus par le modele."""
    return len(encoder.encode(texte))


# Le meme contenu, deux langues : le budget n'est pas le meme.
en = "The retrieval system returns relevant documents."
fr = "Le systeme de recuperation renvoie les documents pertinents."

print(compter_tokens(en), compter_tokens(fr))
# L'ecart typique EN -> FR se situe autour de 1,3x a 1,5x.

# En production, on branche ce compteur DANS le splitter :
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size      = 640,          # budget FR ajuste (au lieu de 512)
    chunk_overlap   = 64,           # 10 % de la taille
    length_function = compter_tokens,   # <-- la ligne qui change tout
    separators      = ["\n\n", "\n", ". ", " ", ""],
)
