from chonkie import TableChunker

# TableChunker respecte la regle : un tableau tient dans un seul
# chunk s'il rentre dans le budget ; sinon il decoupe par groupes
# de lignes EN REPETANT l'en-tete dans chaque fragment.
chunker = TableChunker(
    tokenizer="cl100k_base",
    chunk_size=800,          # budget par chunk
    repeat_header=True,      # <-- la ligne qui evite les colonnes anonymes
)

tableau_markdown = """
| Client   | Montant | Statut   |
|----------|---------|----------|
| Dupont   | 15000   | Regle    |
| Martin   | 8200    | En cours |
...
"""

chunks = chunker.chunk(tableau_markdown)

for c in chunks:
    # Chaque fragment contient encore la ligne d'en-tete :
    # "Ligne 12 : Client=Dupont, Montant=15000, Statut=Regle"
    # reste interpretable isolement, meme hors contexte.
    print(c.text[:80], "...")
