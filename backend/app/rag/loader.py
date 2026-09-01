from pathlib import Path

from langchain_core.documents import Document


def load_patient_documents(patient_folder: str):
    """
    Loads all report text files from a patient's folder
    and returns LangChain Documents.
    """

    patient_path = Path(patient_folder)

    report_files = [
        "blood_report.txt",
        "ct_report.txt",
        "mri_report.txt",
        "xray_report.txt",
        "ecg_report.txt"
    ]

    documents = []

    for filename in report_files:

        file_path = patient_path / filename

        if not file_path.exists():
            continue

        with open(file_path, "r", encoding="utf-8") as file:

            text = file.read()

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "patient_id": patient_path.name,
                        "report_type": filename.replace(".txt", ""),
                        "source": str(file_path)
                    }
                )
            )

    print(
        f"Loaded {len(documents)} reports for {patient_path.name}"
    )

    return documents