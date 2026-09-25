from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI


def envelopper_avec_compression(retriever_de_base):
    """Ajoute une etape d'elagage a un retriever existant.

    Le compresseur recoit chaque chunk recupere et n'en renvoie
    que les passages utiles a la question. Un chunk juge
    totalement hors sujet est ecarte.

    Cout : un appel de modele leger PAR CHUNK. Avec 5 chunks,
    comptez 5 appels supplementaires - parallelisables, mais
    reels. A mesurer avant de deployer.
    """
    extracteur = LLMChainExtractor.from_llm(
        ChatOpenAI(model="gpt-4o-mini", temperature=0)
    )

    return ContextualCompressionRetriever(
        base_compressor=extracteur,
        base_retriever=retriever_de_base,
    )
