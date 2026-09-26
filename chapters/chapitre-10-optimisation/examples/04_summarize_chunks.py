"""Résumé sélectif des chunks longs avec un modèle OpenAI léger."""

from __future__ import annotations

import os
from collections.abc import Callable, Sequence


def compter_tokens_approximatifs(text: str) -> int:
    return max(1, (len(text) + 3) // 4)


def resumer_chunks(
    chunks: Sequence[str],
    resumer: Callable[[str], str],
    *,
    seuil_tokens: int = 500,
    mots_max: int = 100,
) -> list[str]:
    """Ne paie un résumé que pour les chunks qui dépassent le seuil."""

    if seuil_tokens <= 0 or mots_max <= 0:
        raise ValueError("Les seuils doivent être strictement positifs")
    outputs = []
    for chunk in chunks:
        if compter_tokens_approximatifs(chunk) <= seuil_tokens:
            outputs.append(chunk)
            continue
        prompt = (
            f"Résume le texte suivant en {mots_max} mots maximum. "
            "Conserve les faits, chiffres, conditions et exceptions.\n\n"
            f"{chunk}"
        )
        outputs.append(resumer(prompt))
    return outputs


def resumer_avec_openai(*, client=None, model: str | None = None) -> Callable[[str], str]:
    selected_model = model or os.getenv("OPENAI_SMALL_MODEL") or os.getenv("OPENAI_MODEL")
    if not selected_model:
        raise RuntimeError("Configurez OPENAI_SMALL_MODEL ou OPENAI_MODEL")
    if client is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
        from openai import OpenAI

        client = OpenAI()

    def summarize(prompt: str) -> str:
        response = client.responses.create(model=selected_model, input=prompt)
        return str(response.output_text)

    return summarize


if __name__ == "__main__":
    print("Exemple prêt : injectez resumer_avec_openai() dans resumer_chunks().")
