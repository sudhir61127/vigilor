import json
from pathlib import Path

from app.database.connection import get_database

db = get_database()
patients = db["patients"]


def seed_database():
    # Delete existing patients
    patients.delete_many({})

    # backend/patient_documents
    patient_documents = Path(__file__).resolve().parents[2] / "patient_documents"

    patient_list = []

    # Read all patient folders
    for patient_folder in sorted(patient_documents.iterdir()):

        if not patient_folder.is_dir():
            continue

        patient_json = patient_folder / "patient.json"

        if patient_json.exists():

            with open(patient_json, "r", encoding="utf-8") as file:
                patient = json.load(file)
                patient_list.append(patient)

                print(f"Loaded {patient['patient_id']}")

    if not patient_list:
        print("❌ No patient.json files found.")
        return

    patients.insert_many(patient_list)

    print(f"\n✅ Successfully inserted {len(patient_list)} patients.")


if __name__ == "__main__":
    seed_database()