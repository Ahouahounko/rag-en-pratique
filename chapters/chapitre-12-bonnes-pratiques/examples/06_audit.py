from dataclasses import dataclass


@dataclass
class Constat:
    critique: bool
    message: str


def auditer_configuration(config: dict) -> list[Constat]:
    """Verifie ce qui peut l'etre sans jeu de reference ni appel modele.

    config attendu, a titre d'exemple :
        {
            "temperature": 0.0,
            "modele_embedding_ingestion": "text-embedding-3-large",
            "modele_embedding_requete": "text-embedding-3-large",
            "prompt_contient_clause_refus": True,
            "prompt_contient_clause_citation": True,
            "journalise_scores_retrieval": True,
            "journalise_question_reformulee": True,
            "filtrage_acces_au_retrieval": True,
            "k": 5,
        }
    """
    constats = []

    # --- Anti-pattern : temperature > 0 en usage factuel ---
    if config.get("temperature", 0) > 0:
        constats.append(Constat(True,
            f"Temperature a {config['temperature']} : non reproductible, "
            f"a ramener a 0 pour un usage factuel."))

    # --- Anti-pattern : deux modeles d'embedding differents ---
    emb_ingestion = config.get("modele_embedding_ingestion")
    emb_requete = config.get("modele_embedding_requete")
    if emb_ingestion and emb_requete and emb_ingestion != emb_requete:
        constats.append(Constat(True,
            f"Modeles d'embedding differents a l'ingestion "
            f"({emb_ingestion}) et a la requete ({emb_requete}) : "
            f"resultats silencieusement absurdes."))

    # --- Anti-pattern : prompt sans clauses non negociables ---
    if not config.get("prompt_contient_clause_refus"):
        constats.append(Constat(True,
            "Aucune clause de refus detectee dans le prompt systeme."))
    if not config.get("prompt_contient_clause_citation"):
        constats.append(Constat(False,
            "Aucune clause de citation detectee : reponses inverifiables."))

    # --- Anti-pattern : journalisation incomplete ---
    if not config.get("journalise_scores_retrieval"):
        constats.append(Constat(True,
            "Les scores de retrieval ne sont pas journalises : "
            "diagnostic d'incident impossible a posteriori."))
    if not config.get("journalise_question_reformulee"):
        constats.append(Constat(False,
            "La question reformulee n'est pas journalisee separement."))

    # --- Anti-pattern : k eleve sans justification mesuree ---
    if config.get("k", 5) > 10:
        constats.append(Constat(False,
            f"k={config['k']} : verifiez que ce choix vient d'un "
            f"balayage mesure, pas d'un reflexe."))

    # --- Anti-pattern : pas de controle d'acces au retrieval ---
    if not config.get("filtrage_acces_au_retrieval"):
        constats.append(Constat(True,
            "Aucun filtrage par droits au retrieval : tout utilisateur "
            "authentifie peut recuperer n'importe quel passage indexe."))

    return constats


# Utilisation :
#
# constats = auditer_configuration(config)
# critiques = [c for c in constats if c.critique]
# print(f"{len(critiques)} constat(s) critique(s) sur {len(constats)}.")
# for c in constats:
#     marque = "[CRITIQUE]" if c.critique else "[a surveiller]"
#     print(f"{marque} {c.message}")
