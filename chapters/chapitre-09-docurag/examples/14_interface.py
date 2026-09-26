"""Interface Streamlit connectée à l'API DocuRAG."""

from __future__ import annotations

import os

import requests
import streamlit as st

API_URL = os.getenv("DOCURAG_API_URL", "http://localhost:8000")

st.set_page_config(page_title="DocuRAG", page_icon="📚")
st.title("DocuRAG — assistant documentaire")

department = st.sidebar.selectbox(
    "Département",
    ["Tous", "RH", "finance", "juridique", "IT", "produit"],
)

question = st.chat_input("Posez votre question sur les documents…")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Recherche et génération…"):
            payload = {"question": question}
            if department != "Tous":
                payload["department"] = department
            response = requests.post(
                f"{API_URL}/query",
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            payload = response.json()
        st.write(payload["answer"])
        st.caption(
            f"Confiance : {payload['confidence']} — "
            f"{payload['passage_count']} passage(s) — {payload['duration_ms']} ms"
        )
        with st.expander("Sources"):
            for source in payload["sources"]:
                st.caption(
                    f"{source['document']} — pertinence {source['relevance']}"
                )
