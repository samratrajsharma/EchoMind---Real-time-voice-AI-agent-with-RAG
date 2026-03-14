from sentence_transformers import SentenceTransformer
from backend.vector_db.qdrant_client import client
from backend.config import QDRANT_COLLECTION
from rank_bm25 import BM25Okapi

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(query: str, k: int = 3):

    query_vector = model.encode(query).tolist()

    vector_results = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vector,
        limit=10
    )

    chunks = []
    sources = []

    for point in vector_results.points:

        payload = point.payload

        chunks.append(payload["text"])

        sources.append(
            f"{payload['source']} (chunk {payload['chunk_id']})"
        )

    tokenized_corpus = [chunk.split() for chunk in chunks]

    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = query.split()

    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(chunks, sources, scores),
        key=lambda x: x[2],
        reverse=True
    )

    top_chunks = ranked[:k]

    contexts = [item[0] for item in top_chunks]

    final_sources = [item[1] for item in top_chunks]

    return "\n".join(contexts), final_sources