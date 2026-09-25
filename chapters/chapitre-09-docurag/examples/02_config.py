# src/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration unique de DocuRAG.

    Toutes les valeurs viennent de l'environnement ou du fichier
    .env. Pydantic VALIDE les types au demarrage : une faute de
    frappe ou une valeur aberrante fait echouer l'application
    immediatement, au lieu de produire un comportement etrange
    trois heures plus tard.
    """

    # --- Modele de generation ---
    llm_provider: str = "openai"          # interchangeable
    llm_model: str = "gpt-4o"
    llm_temperature: float = 0.0          # reproductibilite
    llm_max_tokens: int = 1024
    openai_api_key: str = ""              # jamais de valeur ici

    # --- Embeddings ---
    embedding_model: str = "BAAI/bge-m3"
    embedding_device: str = "cpu"         # "cuda" si GPU disponible

    # --- Base vectorielle ---
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "docurag_documents"

    # --- Decoupage (cf. chapitre sur le chunking) ---
    chunk_size: int = 512
    chunk_overlap: int = 64

    # --- Retrieval (cf. chapitre sur le retrieval avance) ---
    retrieval_initial_k: int = 20         # candidats avant re-ranking
    retrieval_final_k: int = 5            # passages injectes au modele
    retrieval_score_threshold: float = 0.3
    rerank_score_threshold: float = 0.0   # en dessous : abstention
    use_hybrid_search: bool = True
    use_reranking: bool = True
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    # --- Application ---
    app_name: str = "DocuRAG"
    app_version: str = "1.0.0"
    documents_path: str = "./documents"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Instance unique, mise en cache.

    On appelle TOUJOURS get_settings(), jamais Settings()
    directement : sans le cache, chaque appel relirait le fichier
    et rien ne garantirait que deux modules voient la meme valeur.
    """
    return Settings()
