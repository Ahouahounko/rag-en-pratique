"""Générer une requête SQL avec OpenAI puis l'exécuter en lecture seule."""

from __future__ import annotations

import os
import re
import sqlite3
from typing import Any


def valider_select(requete: str, tables_autorisees: set[str]) -> str:
    """Accepte une seule instruction SELECT et un périmètre de tables explicite."""
    sql = requete.strip().removeprefix("```sql").removesuffix("```").strip().rstrip(";")
    if ";" in sql or not re.match(r"(?is)^select\b", sql):
        raise ValueError("Seule une instruction SELECT unique est autorisée")
    tables = set(re.findall(r"(?i)\b(?:from|join)\s+([a-z_][\w]*)", sql))
    if not tables or not tables <= tables_autorisees:
        raise ValueError(f"Table non autorisée : {sorted(tables - tables_autorisees)}")
    return sql


def question_vers_sql(
    question: str,
    schema: str,
    *,
    client: Any | None = None,
    model: str | None = None,
) -> str:
    if client is None:
        from openai import OpenAI

        client = OpenAI()
    model = model or os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Définissez OPENAI_MODEL.")
    reponse = client.responses.create(
        model=model,
        input=(
            "Produis une seule requête SQLite SELECT, sans commentaire ni Markdown. "
            f"Schéma : {schema}\nQuestion : {question}"
        ),
    )
    return reponse.output_text


def construire_text_to_sql(
    connexion: sqlite3.Connection,
    tables_autorisees: set[str],
    *,
    client: Any | None = None,
    model: str | None = None,
):
    schema = "\n".join(
        ligne[0]
        for ligne in connexion.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"
        )
    )

    def interroger(question: str) -> dict[str, object]:
        brute = question_vers_sql(question, schema, client=client, model=model)
        sql = valider_select(brute, tables_autorisees)
        return {"requete": sql, "resultat": connexion.execute(sql).fetchall()}

    return interroger


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_MODEL"):
        print("Exemple prêt : définissez OPENAI_API_KEY et OPENAI_MODEL.")
    else:
        base = sqlite3.connect(":memory:")
        base.executescript("CREATE TABLE ventes(produit TEXT, montant REAL); INSERT INTO ventes VALUES ('A', 12.5), ('B', 7.5);")
        print(construire_text_to_sql(base, {"ventes"})("Quel est le total des ventes ?"))
