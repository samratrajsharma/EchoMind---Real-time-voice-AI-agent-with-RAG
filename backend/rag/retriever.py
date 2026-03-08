from sentence_transformers import SentenceTransformer
from backend.vector_db.qdrant_client import client
from backend.config import QDRANT_COLLECTION

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_context(query: str, k: int = 3):

    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vector,
        limit=k
    )

    contexts = []
    sources = []

    for point in results.points:

        payload = point.payload

        contexts.append(payload["text"])

        sources.append({
            "source": payload["source"],
            "chunk_id": payload["chunk_id"]
        })

    return "\n".join(contexts), sources