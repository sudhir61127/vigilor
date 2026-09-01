from pathlib import Path

from app.rag.rag_pipeline import build_rag_pipeline


def main():
    # Path to backend/patient_documents
    patient_documents = Path(__file__).parent / "patient_documents"

    if not patient_documents.exists():
        raise FileNotFoundError(
            f"Patient documents folder not found: {patient_documents}"
        )

    print("🚀 Building RAG vector database...\n")

    build_rag_pipeline(str(patient_documents))

    print("\n✅ RAG build completed successfully!")
    print("📁 FAISS index saved in: patient_indexes/")


if __name__ == "__main__":
    main()