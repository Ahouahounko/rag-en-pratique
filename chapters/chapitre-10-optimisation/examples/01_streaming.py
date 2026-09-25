import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI

app = FastAPI()


async def flux_reponse(question: str, retriever, gabarit: str):
    """Genere la reponse en flux.

    Le retrieval et la construction du prompt restent synchrones :
    ils durent moins de 300 ms au total, donc l'utilisateur voit
    du texte apparaitre avant meme de remarquer l'attente.
    """
    passages = retriever.chercher(question)
    contexte = "\n\n".join(p.texte for p in passages)
    prompt = gabarit.format(contexte=contexte, question=question)

    modele = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)

    async for fragment in modele.astream(prompt):
        if fragment.content:
            yield f"data: {fragment.content}\n\n"

    # Les sources partent APRES le texte : l'interface les affiche
    # sous la reponse une fois celle-ci complete.
    sources = [{"source": p.source, "page": p.page} for p in passages]
    yield f"data: {json.dumps({'sources': sources})}\n\n"
    yield "data: [FIN]\n\n"


@app.post("/query/stream")
async def interroger_en_flux(requete: dict):
    return StreamingResponse(
        flux_reponse(requete["question"],
                     app.state.retriever,
                     app.state.gabarit),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            # Sans cette ligne, Nginx tamponne la reponse et
            # l'utilisateur recoit tout d'un bloc a la fin :
            # tout le benefice du streaming disparait.
            "X-Accel-Buffering": "no",
        },
    )
