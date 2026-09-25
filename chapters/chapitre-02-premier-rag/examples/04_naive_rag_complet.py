import os
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Chargement securise : la cle API ne doit JAMAIS etre codee en dur
load_dotenv()

# ============================================================
# PHASE OFFLINE - Ingestion (executee une seule fois, en amont)
# ============================================================

def build_knowledge_base(documents_path: str) -> FAISS:
    """Charge, decoupe, encode et indexe les documents."""
    loader = DirectoryLoader(documents_path,
                             glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, chunk_overlap=64,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vector_store = FAISS.from_documents(chunks, embedding_model)
    vector_store.save_local("faiss_index")
    print(f"[Ingestion] {len(chunks)} chunks indexes.")
    return vector_store


# ============================================================
# PHASE ONLINE - Retrieval + Generation (par requete utilisateur)
# ============================================================

def build_naive_rag_chain(vector_store: FAISS) -> RetrievalQA:
    """Assemble la chaine RAG naif : retriever + prompt + LLM."""

    # Retriever : top-4 chunks par similarite cosinus
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # Prompt avec grounding strict et instruction de citation
    prompt_template = """Tu es un assistant expert et rigoureux.
Reponds a la question en te basant UNIQUEMENT sur les extraits fournis.
Si la reponse est absente des extraits, indique-le clairement.
Ne fabrique aucune information. Cite tes sources (document et page).

Extraits :
{context}

Question : {question}

Reponse :"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0  # Deterministe : fidelite factuelle maximale
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",           # Concatene tous les chunks dans le prompt
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True  # Pour la tracabilite
    )


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():
    """Boucle interactive du RAG naif."""
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Charger l'index s'il existe, sinon le construire
    if os.path.exists("faiss_index"):
        vector_store = FAISS.load_local("faiss_index", embedding_model)
        print("[Main] Index charge depuis le disque.")
    else:
        vector_store = build_knowledge_base("./documents/")

    rag_chain = build_naive_rag_chain(vector_store)
    print("\n" + "=" * 55)
    print(" RAG naif - Assistant documentaire (tapez 'fin' pour quitter)")
    print("=" * 55)

    while True:
        question = input("\nVotre question : ").strip()
        if question.lower() in ["fin", "quitter", "exit"]:
            break
        if not question:
            continue

        result = rag_chain({"query": question})
        print(f"\nReponse :\n{result['result']}")
        print("\nSources consultees :")
        for i, doc in enumerate(result["source_documents"], 1):
            print(f" [{i}] {doc.metadata.get('source', '?')} "
                  f"- p.{doc.metadata.get('page', '?')}")
        print("-" * 55)


if __name__ == "__main__":
    main()
