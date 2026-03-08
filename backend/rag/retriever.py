from sentence_transformers import SentenceTransformer
from backend.vector_db.qdrant_client import client
from backend.config import QDRANT_COLLECTION

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_context(query: str, k: int = 3):
    """
    Retrieve the most relevant chunks from Qdrant using semantic search.
    """

    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vector,
        limit=k
    )

    contexts = []

    for point in results.points:
        if "text" in point.payload:
            contexts.append(point.payload["text"])

    return "\n".join(contexts)