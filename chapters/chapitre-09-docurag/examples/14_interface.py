# src/interface/app.py
import os

import requests
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="DocuRAG", page_icon=":books:",
                   layout="centered")
st.title("DocuRAG - assistant documentaire")

# --- Barre laterale : filtres et etat du service ---
with st.sidebar:
    st.header("Filtres")
    departement = st.selectbox(
        "Departement",
        ["Tous", "RH", "finance", "juridique", "IT", "produit"],
    )

    st.divider()
    try:
        sante = requests.get(f"{API}/health", timeout=3).json()
        st.success(f"Service actif - {sante['collection']['points']} "
                   f"passages indexes")
    except Exception:
        st.error("Service indisponible")

# --- Historique de la conversation ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["contenu"])
        if message.get("sources"):
            with st.expander("Sources"):
                for numero, source in enumerate(message["sources"], 1):
                    st.caption(
                        f"[doc_{numero}] {source['document']} "
                        f"- page {source['page']} "
                        f"(pertinence {source['pertinence']})"
                    )

# --- Nouvelle question ---
if question := st.chat_input("Posez votre question..."):
    st.session_state.messages.append(
        {"role": "user", "contenu": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents..."):
            charge = {"question": question}
            if departement != "Tous":
                charge["departement"] = departement

            try:
                reponse = requests.post(f"{API}/query", json=charge,
                                        timeout=60).json()
            except Exception as erreur:
                st.error(f"Erreur : {erreur}")
                st.stop()

        st.markdown(reponse["reponse"])

        # La confiance est TOUJOURS affichee : c'est ce qui invite
        # l'utilisateur a verifier quand le systeme est peu sur.
        couleur = {"Haut": "green", "Moyen": "orange", "Bas": "red"}
        st.caption(
            f":{couleur[reponse['confiance']]}[Confiance : "
            f"{reponse['confiance']}] - {reponse['nb_passages']} "
            f"passages - {reponse['duree_ms']} ms"
        )

        if reponse["sources"]:
            with st.expander("Sources"):
                for numero, source in enumerate(reponse["sources"], 1):
                    st.caption(
                        f"[doc_{numero}] {source['document']} "
                        f"- page {source['page']}"
                    )

    st.session_state.messages.append({
        "role": "assistant",
        "contenu": reponse["reponse"],
        "sources": reponse["sources"],
    })
