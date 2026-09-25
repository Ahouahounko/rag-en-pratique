from langchain.document_loaders import (
    PyPDFLoader, UnstructuredWordDocumentLoader,
    WebBaseLoader, DirectoryLoader
)

# PDF : un Document par page, avec metadata['page']
pdf_docs = PyPDFLoader("rapport_annuel.pdf").load()

# Word : un Document par fichier
word_docs = UnstructuredWordDocumentLoader("contrat.docx").load()

# Page web : recupere et nettoie le HTML
web_docs = WebBaseLoader("https://exemple.com/faq").load()

# Dossier entier : charge tous les PDF recursivement
all_docs = DirectoryLoader(
    "./documents/", glob="**/*.pdf", loader_cls=PyPDFLoader
).load()

print(f"{len(all_docs)} documents charges, prets pour le chunking.")
