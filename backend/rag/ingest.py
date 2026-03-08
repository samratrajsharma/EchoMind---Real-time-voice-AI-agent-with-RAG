import uuid
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct

from backend.vector_db.qdrant_client import client
from backend.config import QDRANT_COLLECTION

model = SentenceTransformer("all-MiniLM-L6-v2")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


def ingest_document(text, source):

    chunks = splitter.split_text(text)

    vectors = model.encode(chunks)

    points = []

    for chunk, vector in zip(chunks, vectors):

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector.tolist(),
                payload={
                    "text": chunk,
                    "source": source
                }
            )
        )

    client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=points
    )

    return len(points)