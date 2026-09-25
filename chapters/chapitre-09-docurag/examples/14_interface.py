"""Interface Streamlit connectée à l'API DocuRAG."""

from __future__ import annotations

import os

import requests
import streamlit as st

API_URL = os.getenv("DOCURAG_API_URL", "http://localhost:8000")

st.set_page_config(page_title="DocuRAG", page_icon="📚")
st.title("DocuRAG — assistant documentaire OpenAI")

question = st.chat_input("Posez votre question sur les documents…")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Recherche et génération OpenAI…"):
            response = requests.post(
                f"{API_URL}/query",
                json={"question": question, "top_k": 3},
                timeout=120,
            )
            response.raise_for_status()
            payload = response.json()
        st.write(payload["answer"])
        with st.expander("Sources"):
            for source in payload["sources"]:
                st.caption(
                    f"{source['metadata'].get('source', 'document')} "
                    f"— score {source['score']}"
                )
