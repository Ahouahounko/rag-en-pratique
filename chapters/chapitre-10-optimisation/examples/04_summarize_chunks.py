from typing import List

def summarize_chunks(chunks: List[str], llm) -> List[str]:
    """
    Resume chaque chunk trop long pour reduire les tokens envoyes
    au modele principal. Utiliser un LLM leger (ex. gpt-4o-mini).
    """
    summaries = []

    for chunk in chunks:
        # Estimer si le chunk est trop long
        token_count = len(chunk) // 4   # approximation grossiere

        if token_count > 500:
            summary_prompt = f"""
Resume ce texte en maximum 100 mots,
en gardant les informations essentielles :

{chunk}

Resume :"""
            summary = llm.invoke(summary_prompt)
            summaries.append(summary)
        else:
            summaries.append(chunk)

    return summaries
