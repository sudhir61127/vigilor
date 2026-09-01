import pickle
from pathlib import Path

import faiss
import numpy as np

INDEX_PATH = Path("patient_indexes/faiss_index.index")
METADATA_PATH = Path("patient_indexes/faiss_metadata.pkl")


def build_vector_store(chunks, embeddings):
    """
    Build and save a FAISS vector database.
    """

    INDEX_PATH.parent.mkdir(exist_ok=True)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    metadata = []

    for chunk in chunks:
        metadata.append(
            {
                "content": chunk.page_content,
                "metadata": chunk.metadata,
            }
        )

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"✅ Indexed {len(metadata)} chunks.")


def load_vector_store():
    """
    Load FAISS index and metadata.
    """

    if not INDEX_PATH.exists():
        raise FileNotFoundError("FAISS index not found.")

    index = faiss.read_index(str(INDEX_PATH))

    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata