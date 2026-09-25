from pinecone import Pinecone, ServerlessSpec
import os

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

if "rag-production" not in pc.list_indexes().names():
    pc.create_index(
        name="rag-production",
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="eu-west-1",   # hebergement europeen : contrainte RGPD
        ),
    )

index = pc.Index("rag-production")

# Insertion par lots de 100 maximum : au-dela, la requete
# depasse frequemment la taille limite acceptee.
index.upsert(
    vectors=[{
        "id": "chunk_001",
        "values": vecteur,                     # 1536 dimensions
        "metadata": {
            "source": "rapport_annuel_2024.pdf",
            "page": 15,
            "departement": "finance",
            "texte": "Le chiffre d'affaires annuel atteint...",
        },
    }],
    namespace="finance",
)
