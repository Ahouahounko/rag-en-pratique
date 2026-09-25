def formater_balise(passages: list) -> str:
    """Assemble les passages dans une structure balisee.

    A privilegier quand les metadonnees comptent pour la reponse
    (dates de revision, niveau de confidentialite, service
    emetteur) ou quand le prompt contient deja beaucoup de texte.
    """
    lignes = ["<extraits>"]

    for numero, passage in enumerate(passages, start=1):
        meta = passage.metadata
        lignes.append(f"""  <extrait id="doc_{numero}">
    <source>{meta.get("source", "inconnu")}</source>
    <page>{meta.get("page", "?")}</page>
    <date_revision>{meta.get("date", "non precisee")}</date_revision>
    <service>{meta.get("departement", "non precise")}</service>
    <contenu>
{passage.page_content}
    </contenu>
  </extrait>""")

    lignes.append("</extraits>")
    return "\n".join(lignes)


# L'instruction systeme doit RENVOYER a la structure, sinon
# le balisage n'est qu'un cout en tokens supplementaire.
SYSTEME_BALISE = """Tes reponses s'appuient exclusivement sur les
extraits contenus dans les balises <extraits>.
Pour citer, utilise l'attribut id : [doc_2].
Le champ <date_revision> fait autorite en cas de contradiction
entre deux extraits : le plus recent prevaut."""
