from pydantic import BaseModel, Field
from typing import List, Optional


class Patient(BaseModel):
    patient_id: str
    full_name: str
    age: int
    gender: str

    blood_group: str
    allergies: List[str] = []

    diagnosis: str

    mri_report: Optional[str] = None
    ct_report: Optional[str] = None

    blood_reports: List[str] = []

    previous_surgeries: List[str] = []

    medications: List[str] = []

    emergency_contact: str