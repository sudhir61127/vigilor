"""
Patient Tool for retrieving patient information from the database.
"""

from typing import Optional, List
import json
from pathlib import Path


def get_sample_patients() -> dict:
    """
    Load sample patient data from patient_documents folder.
    This provides demo data without requiring MongoDB.
    """
    patients_data = {}
    patient_docs_path = Path("backend/patient_documents")
    
    if patient_docs_path.exists():
        for patient_folder in sorted(patient_docs_path.iterdir()):
            if not patient_folder.is_dir():
                continue
            
            patient_json = patient_folder / "patient.json"
            if patient_json.exists():
                with open(patient_json, "r") as f:
                    patient_data = json.load(f)
                    # Normalize patient ID for lookup
                    patient_id = patient_data.get("patient_id", "").replace("-", "")
                    patients_data[patient_id] = patient_data
                    # Also store by folder name
                    patients_data[patient_folder.name] = patient_data
    
    return patients_data


# Cache sample patients at module load
_SAMPLE_PATIENTS = get_sample_patients()


def search_patient(patient_id: str) -> dict:
    """
    Search for a patient by ID.
    
    Args:
        patient_id: Patient identifier (e.g., 'P001', 'PAT001', 'PAT-001')
    
    Returns:
        dict with patient information or error message
    """
    # Normalize the patient ID for searching
    patient_id_clean = patient_id.replace("-", "").replace("PAT", "")
    
    # Try different formats
    search_formats = [
        patient_id,  # As provided
        f"PAT{patient_id_clean.zfill(3)}",  # PAT001 format
        f"PAT-{patient_id_clean.zfill(3)}",  # PAT-001 format
        f"PAT001",  # Folder name style
        patient_id.upper(),  # Uppercase
    ]
    
    for search_key in search_formats:
        if search_key in _SAMPLE_PATIENTS:
            patient_data = _SAMPLE_PATIENTS[search_key]
            return {
                "success": True,
                "patient": {
                    "patient_id": patient_data.get("patient_id", patient_id),
                    "name": patient_data.get("patient_name", "Unknown"),
                    "age": patient_data.get("age", "Unknown"),
                    "gender": patient_data.get("gender", "Unknown"),
                    "available_reports": list(patient_data.get("reports", {}).keys()),
                    "available_images": list(patient_data.get("images", {}).keys()),
                }
            }
    
    return {
        "success": False,
        "error": f"Patient {patient_id} not found in the system."
    }


def get_patient_report_list(patient_id: str) -> dict:
    """
    Get list of available reports for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        dict with list of reports or error message
    """
    # Normalize the patient ID
    patient_id_clean = patient_id.replace("-", "").replace("PAT", "")
    
    search_formats = [
        patient_id,
        f"PAT{patient_id_clean.zfill(3)}",
        f"PAT-{patient_id_clean.zfill(3)}",
        f"PAT001",
        patient_id.upper(),
    ]
    
    for search_key in search_formats:
        if search_key in _SAMPLE_PATIENTS:
            patient_data = _SAMPLE_PATIENTS[search_key]
            reports = patient_data.get("reports", {})
            return {
                "success": True,
                "patient_id": patient_id,
                "available_reports": {
                    "types": list(reports.keys()),
                    "total": len(reports)
                }
            }
    
    return {
        "success": False,
        "error": f"Patient {patient_id} not found."
    }


def list_all_patients() -> dict:
    """
    List all available patients in the system.
    
    Returns:
        dict with list of all patients
    """
    unique_patients = {}
    
    for patient_id, patient_data in _SAMPLE_PATIENTS.items():
        patient_name = patient_data.get("patient_name", "Unknown")
        if patient_name not in unique_patients:
            unique_patients[patient_name] = {
                "id": patient_data.get("patient_id", patient_id),
                "name": patient_name,
                "age": patient_data.get("age", "Unknown"),
                "gender": patient_data.get("gender", "Unknown"),
            }
    
    return {
        "success": True,
        "patients": list(unique_patients.values()),
        "total": len(unique_patients)
    }
