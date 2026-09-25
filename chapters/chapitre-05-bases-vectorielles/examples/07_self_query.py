from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain_openai import ChatOpenAI

# Ces descriptions sont lues par le modele. Leur precision
# determine directement la qualite des filtres generes :
# ENUMEREZ les valeurs possibles plutot que de les decrire.
SCHEMA = [
    AttributeInfo(
        name="departement",
        description="Departement proprietaire. Valeurs possibles : "
                    "'RH', 'juridique', 'finance', 'produit', 'IT'.",
        type="string",
    ),
    AttributeInfo(
        name="date",
        description="Date de publication, format AAAA-MM-JJ.",
        type="string",
    ),
    AttributeInfo(
        name="confidentialite",
        description="Niveau d'acces. Valeurs possibles : "
                    "'public', 'interne', 'confidentiel'.",
        type="string",
    ),
]

DESCRIPTION_CORPUS = (
    "Base documentaire interne : politiques RH, contrats, "
    "procedures qualite, rapports financiers, documentation technique."
)


def construire_self_query(base_vectorielle):
    """Retriever capable de generer ses propres filtres."""
    return SelfQueryRetriever.from_llm(
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        vectorstore=base_vectorielle,
        document_contents=DESCRIPTION_CORPUS,
        metadata_field_info=SCHEMA,
        verbose=True,          # affiche les filtres generes : gardez-le
    )
