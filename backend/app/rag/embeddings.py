from sentence_transformers import SentenceTransformer

# Load the embedding model once when the application starts
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """
    Generate an embedding for a single text.
    """
    return embedding_model.encode(text)


def embed_documents(chunks):
    """
    Generate embeddings for a list of LangChain document chunks.
    """
    texts = [chunk.page_content for chunk in chunks]

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings