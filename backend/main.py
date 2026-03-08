from fastapi import FastAPI, UploadFile, File
import os

from backend.vector_db.qdrant_client import init_qdrant
from backend.rag.ingest import ingest_document
from backend.rag.retriever import retrieve_context
from backend.services.llm_service import generate_answer
from backend.config import UPLOAD_DIR

app = FastAPI()


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

    chunks = ingest_document(text, file.filename)

    return {
        "message": "Document processed",
        "chunks": chunks
    }


@app.post("/ask")
def ask_question(query: str):

    context = retrieve_context(query)

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
        "context_used": context
    }