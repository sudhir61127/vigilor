def get_patient(patient_id: str):
    patients = {
        "P001": {
            "patient_id": "P001",
            "name": "Test Patient",
            "age": 45,
            "procedure": "Appendectomy"
        }
    }

    return patients.get(patient_id, {"error": "Patient not found"})