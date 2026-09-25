from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


def construire_rag_conversationnel(base_vectorielle,
                                   plafond_historique: int = 2000):
    """RAG multi-tours dont l'historique ne peut pas exploser.

    plafond_historique : au-dela, les tours les plus anciens sont
    automatiquement condenses en resume. C'est une BORNE, pas une
    cible : la memoire reste en dessous.
    """
    modele = ChatOpenAI(model="gpt-4o", temperature=0)

    memoire = ConversationSummaryBufferMemory(
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),  # leger
        max_token_limit=plafond_historique,
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )

    # Etape 1 : rendre la question autonome grace a l'historique.
    PROMPT_CONDENSATION = ChatPromptTemplate.from_messages([
        ("system", """Reformule la question en une question autonome,
en resolvant les references a l'aide de l'historique.
Si la question est deja autonome, retourne-la inchangee.
Ne reponds pas a la question."""),
        ("human", """Historique :
{chat_history}

Question : {question}

Question autonome :"""),
    ])

    # Etape 2 : repondre a partir des extraits seuls.
    PROMPT_REPONSE = ChatPromptTemplate.from_messages([
        ("system", SYSTEME),
        ("human", """EXTRAITS :
{context}

QUESTION : {question}

REPONSE :"""),
    ])

    return ConversationalRetrievalChain.from_llm(
        llm=modele,
        retriever=base_vectorielle.as_retriever(search_kwargs={"k": 4}),
        memory=memoire,
        condense_question_prompt=PROMPT_CONDENSATION,
        combine_docs_chain_kwargs={"prompt": PROMPT_REPONSE},
        return_source_documents=True,
    )
