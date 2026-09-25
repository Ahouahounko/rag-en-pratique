from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def build_knowledge_base(documents_path: str) -> FAISS:
    """
    Pipeline d'ingestion (phase OFFLINE) :
    Charge les PDF -> Decoupe en chunks -> Encode en vecteurs -> Indexe.
    """
    # Etape 1 : Chargement
    loader = DirectoryLoader(
        documents_path, glob="**/*.pdf", loader_cls=PyPDFLoader
    )
    documents = loader.load()
    print(f"[Ingestion] {len(documents)} pages chargees")

    # Etape 2 : Chunking avec chevauchement (overlap)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=64,   # ~12,5 % d'overlap
        separators=["\n\n", "\n", ".", " ", ""]  # Respecte les frontieres naturelles
    )
    chunks = splitter.split_documents(documents)
    print(f"[Ingestion] {len(chunks)} chunks crees")

    # Etape 3 : Encodage (modele multilingue adapte au francais)
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"}  # Remplacez par "cuda" si GPU disponible
    )

    # Etape 4 : Construction et sauvegarde de l'index FAISS
    vector_store = FAISS.from_documents(chunks, embedding_model)
    vector_store.save_local("faiss_index")
    print("[Ingestion] Index sauvegarde dans ./faiss_index/")

    return vector_store
