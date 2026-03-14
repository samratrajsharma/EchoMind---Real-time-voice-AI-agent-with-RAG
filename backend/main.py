from fastapi import FastAPI, UploadFile, File
import os
from fastapi.responses import StreamingResponse

from backend.vector_db.qdrant_client import init_qdrant
from backend.rag.ingest import ingest_document
from backend.rag.retriever import retrieve_context
from backend.services.llm_service import generate_answer, stream_generated_answer
from backend.rag.document_loader import load_document
from backend.config import UPLOAD_DIR
from backend.services.memory import ConversationMemory
from livekit import api
from backend.config import LIVEKIT_API_KEY, LIVEKIT_API_SECRET

app = FastAPI()
memory = ConversationMemory()


@app.on_event("startup")
def startup():
    init_qdrant()
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    contents = await file.read()

    text = contents.decode("utf-8", errors="ignore")

    filepath = os.path.join(UPLOAD_DIR, file.filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    text = load_document(filepath)

    chunks = ingest_document(text, file.filename)

    return {
        "message": "Document processed",
        "chunks": chunks
    }


@app.post("/ask")
def ask_question(query: str):

    context, sources = retrieve_context(query)
    history = memory.get_history()
    conversation = ''

    for msg in history:
        converstaion += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
You are an AI assistant.

Use the context to answer the question.

Context:
{context}

Question:
{query}
"""

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "context_used": context,
        "sources" : sources
    }

@app.post('/ask-stream')
def ask_stream(query:str):
    context, sources = retrieve_context(query)

    history = memory.get_history()

    conversation = ''

    for msg in history:
        converstaion += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
You are an AI assistant.

Use the context to answer the question.

Context:
{context}

Question:
{query}
"""

    def stream():
        answer = ''
        for token in stream_generated_answer(prompt):
            answer += token
            yield token
        memory.add('user', query)
        memory.add('assistant', answer)
   
    return StreamingResponse(stream(),media_type = 'text/plain')

@app.get("/livekit-token")
def get_livekit_token(identity: str = "user", room: str = "echomind-room"):

    token = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_name(identity)
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=room,
                can_publish=True,
                can_subscribe=True,
            )
        )
    )

    return {
        "token": token.to_jwt(),
        "room": room
    }