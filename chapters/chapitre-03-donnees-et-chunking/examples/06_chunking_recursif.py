from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size      = 640,               # budget ajuste au francais
    chunk_overlap   = 64,                # 10 %
    length_function = compter_tokens,    # en tokens, cf. listing precedent
    separators = [
        "\n## ",     # <-- titres Markdown D'ABORD : les sections
        "\n### ",    #     restent intactes tant qu'elles tiennent
        "\n\n",      # paragraphes
        "\n",        # lignes
        ". ",        # phrases
        " ",         # mots
        "",          # caracteres (dernier recours)
    ],
)

chunks = splitter.split_text(document)

# Sans les deux premieres lignes de la liste, une section Markdown
# de 300 tokens suivie d'une autre de 400 sera regroupee dans un
# meme chunk de 640 : deux sujets, un seul vecteur, et aucune
# requete ne lui correspondra vraiment.
