from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# Le prompt est le contrat entre vous et le LLM.
# "Grounding" = obligation de rester dans les documents fournis.
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Tu es un assistant expert et rigoureux.

REGLES ABSOLUES :
1. Tu reponds UNIQUEMENT a partir des extraits de documents fournis.
2. Si l'information n'est pas dans les extraits, tu le dis clairement :
   "Cette information n'est pas disponible dans les documents consultes."
3. Tu ne fabriques JAMAIS d'information, meme si elle te semble evidente.
4. Tu cites systematiquement tes sources : [Nom du document, page X]
5. Ton ton : professionnel, precis, concis."""),

    ("human", """EXTRAITS DE DOCUMENTS :
{context}

QUESTION : {question}

REPONSE (avec citations) :""")
])

def generate_answer(question: str,
                    chunks: list,
                    temperature: float = 0.0) -> str:
    """
    Generation de la reponse a partir des chunks recuperes.
    Temperature = 0 pour une fidelite factuelle maximale.
    """
    # Formater les chunks avec leurs metadonnees pour faciliter les citations
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.metadata.get("source", "Document inconnu")
        page = chunk.metadata.get("page", "?")
        context_parts.append(
            f"[Extrait {i} - {source}, page {page}]\n{chunk.page_content}"
        )
    context = "\n\n---\n\n".join(context_parts)

    llm = ChatOpenAI(model="gpt-4o", temperature=temperature)
    chain = RAG_PROMPT | llm | StrOutputParser()

    return chain.invoke({"context": context, "question": question})
