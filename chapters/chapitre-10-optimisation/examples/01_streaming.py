"""Diffusion SSE d'une réponse OpenAI avec sources en dernier événement."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Passage:
    texte: str
    source: str
    page: int = 0


def _client(client=None):
    if client is not None:
        return client
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
    from openai import OpenAI

    return OpenAI()


def evenements_sse(
    question: str,
    passages: Sequence[Passage],
    *,
    model: str | None = None,
    client=None,
) -> Iterator[str]:
    """Émet les deltas de texte, les sources, puis le marqueur de fin."""

    selected_model = model or os.getenv("OPENAI_MODEL")
    if not selected_model:
        raise RuntimeError("Configurez OPENAI_MODEL avant d'activer le streaming")
    contexte = "\n\n".join(
        f"[doc_{index}] {passage.source}, page {passage.page}\n{passage.texte}"
        for index, passage in enumerate(passages, start=1)
    )
    stream: Iterable[object] = _client(client).responses.create(
        model=selected_model,
        instructions=(
            "Réponds uniquement à partir des extraits. "
            "Cite chaque affirmation avec [doc_N]."
        ),
        input=f"EXTRAITS\n{contexte}\n\nQUESTION\n{question}",
        stream=True,
    )
    for event in stream:
        if getattr(event, "type", "") == "response.output_text.delta":
            delta = getattr(event, "delta", "")
            if delta:
                yield f"data: {json.dumps({'delta': delta}, ensure_ascii=False)}\n\n"

    sources = [
        {"source": passage.source, "page": passage.page}
        for passage in passages
    ]
    yield f"data: {json.dumps({'sources': sources}, ensure_ascii=False)}\n\n"
    yield "data: [FIN]\n\n"


def reponse_streaming(question: str, retriever, **kwargs: object):
    """Adaptateur FastAPI facultatif, importé seulement si nécessaire."""

    from fastapi.responses import StreamingResponse

    passages = retriever.chercher(question)
    return StreamingResponse(
        evenements_sse(question, passages, **kwargs),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    print("Exemple prêt : configurez OPENAI_API_KEY et OPENAI_MODEL, puis appelez evenements_sse().")
