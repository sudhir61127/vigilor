from pathlib import Path

from app.rag.loader import load_patient_documents
from app.rag.chunker import split_documents
from app.rag.embeddings import embed_documents
from app.rag.vector_store import build_vector_store


def build_rag_pipeline(patient_documents_folder: str):
    """
    Build the FAISS vector database using all patient reports.
    """

    all_documents = []

    patient_root = Path(patient_documents_folder)

    print("Loading patient reports...")

    for patient_folder in sorted(patient_root.iterdir()):

        if not patient_folder.is_dir():
            continue

        documents = load_patient_documents(str(patient_folder))

        all_documents.extend(documents)

    print(f"Loaded {len(all_documents)} reports.")

    print("Splitting reports into chunks...")

    chunks = split_documents(all_documents)

    print(f"Created {len(chunks)} chunks.")

    print("Generating embeddings...")

    embeddings = embed_documents(chunks)

    print("Building FAISS index...")

    build_vector_store(chunks, embeddings)

    print("\n✅ RAG pipeline completed successfully.")