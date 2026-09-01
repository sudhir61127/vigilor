from app.database.connection import get_database

# Get database instance
db = get_database()

# Patients collection
patients = db["patients"]


def create_patient(patient_data: dict):
    """
    Insert a new patient into MongoDB.
    """
    return patients.insert_one(patient_data)


def get_patient_by_id(patient_id: str):
    """
    Find a patient using patient_id.
    """
    patient = patients.find_one({"patient_id": patient_id})
    return patient if patient else None


def get_patient_by_name(name: str):
    """
    Find a patient using full_name.
    """
    patient = patients.find_one({"full_name": name})
    return patient if patient else None


def update_patient(patient_id: str, updated_data: dict):
    """
    Update patient details.
    """
    return patients.update_one(
        {"patient_id": patient_id},
        {"$set": updated_data}
    )


def delete_patient(patient_id: str):
    """
    Delete a patient.
    """
    return patients.delete_one({"patient_id": patient_id})


def get_all_patients() -> list:
    """
    Return all patients.
    """
    return list(patients.find())


def search_patients(query: dict) -> list:
    """
    Search patients using any MongoDB query.
    
    Examples:
        search_patients({"blood_group": "B+"})
        search_patients({"diagnosis": "Diabetes"})
        search_patients({"gender": "Female"})
    """
    return list(patients.find(query))