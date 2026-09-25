import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_db")

fonction_embedding = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],   # jamais en dur dans le code
    model_name="text-embedding-3-small",
)

collection = client.get_or_create_collection(
    name="base_documentaire",
    embedding_function=fonction_embedding,
    metadata={"hnsw:space": "cosine"},      # metrique explicite
)

collection.add(
    documents=[
        "La garantie standard couvre 24 mois a compter de la livraison.",
        "Le remboursement peut etre demande sous 30 jours.",
    ],
    metadatas=[
        {"source": "cgv.pdf", "page": 8,  "departement": "juridique"},
        {"source": "cgv.pdf", "page": 12, "departement": "juridique"},
    ],
    ids=["chunk_001", "chunk_002"],
)

resultats = collection.query(
    query_texts=["politique de remboursement"],
    n_results=3,
    where={"departement": "juridique"},     # filtre structurel
)
