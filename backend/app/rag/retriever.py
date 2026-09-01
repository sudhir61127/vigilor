import numpy as np

from app.rag.embeddings import get_embedding
from app.rag.vector_store import load_vector_store


def search_documents(query: str, top_k: int = 3):
    """
    Search the FAISS vector database and return the
    most relevant document chunks.
    """

    index, metadata = load_vector_store()

    query_embedding = np.array(
        [get_embedding(query)],
        dtype="float32"
    )

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        result = metadata[idx].copy()
        result["score"] = float(distance)

        results.append(result)

    return results