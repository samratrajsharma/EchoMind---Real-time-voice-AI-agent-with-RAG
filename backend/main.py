from fastapi import FastAPI, UploadFile, File
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time

from backend.vector_db.qdrant_client import init_qdrant
from backend.rag.ingest import ingest_document
from backend.rag.retriever import retrieve_context
from backend.services.llm_service import generate_answer, stream_generated_answer
from backend.rag.document_loader import load_document
from backend.config import UPLOAD_DIR
from backend.services.memory import ConversationMemory

app = FastAPI()
memory = ConversationMemory()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Sources", "X-Rag-Latency", "X-Trace"]
)

@app.on_event("startup")
def startup():
    init_qdrant()
    os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    contents = await file.read()

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

    conversation = ""

    for msg in history:
        conversation += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
You are an AI assistant.

Use the context to answer the question.

Conversation History:
{conversation}

Context:
{context}

Question:
{query}
"""

    answer = generate_answer(prompt)

    memory.add_user_message(query)
    memory.add_ai_message(answer)

    return {
        "answer": answer,
        "context_used": context,
        "sources": sources
    }

@app.get("/ask-stream")
def ask_stream(query: str):

    start_time = time.time()

    trace = []
    trace.append("User query received")
    trace.append("Retrieving relevant documents")

    context, sources = retrieve_context(query)

    rag_time = int((time.time() - start_time) * 1000)

    trace.append(f"Retrieved {len(sources)} document chunks")
    trace.append("Generating answer with LLM")

    prompt = f"""
Answer the question using the context.

Context:
{context}

Question:
{query}
"""

    def stream():
        for token in stream_generated_answer(prompt):
            yield token

    return StreamingResponse(
        stream(),
        media_type="text/plain",
        headers={
            "X-Sources": ",".join(sources),
            "X-Rag-Latency": str(rag_time),
            "X-Trace": "|".join(trace)
        }
    )