from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI


def construire_text_to_sql(uri_base: str):
    """Chaine question -> SQL -> execution -> reponse.

    L'URI DOIT pointer vers un compte en LECTURE SEULE. C'est la
    seule protection reellement fiable : tout le reste (filtrage
    de mots-cles, verification de la requete) peut etre contourne
    par une formulation habile.
    """
    base = SQLDatabase.from_uri(
        uri_base,
        # Perimetre explicite : le modele ne voit que ces tables,
        # donc il ne peut pas en interroger d'autres.
        include_tables=["ventes", "produits", "clients", "commandes"],
        sample_rows_in_table_info=3,   # aide le modele a typer
    )

    modele = ChatOpenAI(model="gpt-4o", temperature=0)
    generer_sql = create_sql_query_chain(modele, base)
    executer = QuerySQLDataBaseTool(db=base)

    return (
        RunnablePassthrough.assign(requete=generer_sql)
        | RunnablePassthrough.assign(
            resultat=lambda x: executer.invoke(x["requete"])
        )
    )
