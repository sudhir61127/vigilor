"""
Surgical Checklist Tool for pre-surgical verification.
Provides a standard surgical safety checklist.
"""


def get_surgical_checklist(patient_id: str = None, procedure: str = None) -> dict:
    """
    Generate a pre-surgical checklist with all critical checkpoints.
    
    Args:
        patient_id: Optional patient identifier
        procedure: Optional procedure name
    
    Returns:
        dict with checklist items and completion status
    """
    
    checklist_items = [
        {
            "id": 1,
            "category": "Sign In",
            "items": [
                {
                    "checkbox_id": "sign_in_1",
                    "task": "Confirm patient identity",
                    "description": "Verify patient name, DOB, and medical record number match records",
                    "completed": False,
                    "critical": True
                },
                {
                    "checkbox_id": "sign_in_2",
                    "task": "Confirm surgical site marked",
                    "description": "Verify surgical site has been marked by surgeon with indelible marker",
                    "completed": False,
                    "critical": True
                },
                {
                    "checkbox_id": "sign_in_3",
                    "task": "Consent form verified",
                    "description": "Ensure surgical consent form is signed and in patient's record",
                    "completed": False,
                    "critical": True
                },
                {
                    "checkbox_id": "sign_in_4",
                    "task": "Allergies documented",
                    "description": "Confirm allergies documented and communicated to team",
                    "completed": False,
                    "critical": False
                }
            ]
        },
        {
            "id": 2,
            "category": "Time Out (Before Incision)",
            "items": [
                {
                    "checkbox_id": "timeout_1",
                    "task": "Team introduction",
                    "description": "All team members introduce themselves by name and role",
                    "completed": False,
                    "critical": True
                },
                {
                    "checkbox_id": "timeout_2",
                    "task": "Confirm procedure",
                    "description": "Surgeon confirms procedure name, site, and position",
                    "completed": False,
                    "critical": True
                },
                {
                    "checkbox_id": "timeout_3",
                    "task": "Sterility confirmed",
                    "description": "Verify sterility of instruments and field",
                    "completed": False,
                    "critical": True
                },
                {
                    "checkbox_id": "timeout_4",
                    "task": "Equipment functional",
                    "description": "Confirm all necessary equipment is present and functional",
                    "completed": False,
                    "critical": False
                },
                {
                    "checkbox_id": "timeout_5",
                    "task": "Imaging available",
                    "description": "Ensure all required imaging and reports are available",
                    "completed": False,
                    "critical": False
                }
            ]
        },
        {
            "id": 3,
            "category": "Sign Out (Before Leaving OR)",
            "items": [
                {
                    "checkbox_id": "signout_1",
                    "task": "Specimen labeled",
                    "description": "Confirm any specimens are properly labeled and documented",
                    "completed": False,
                    "critical": False
                },
                {
                    "checkbox_id": "signout_2",
                    "task": "Instrument count verified",
                    "description": "Verify all instruments, sponges, and sharps are accounted for",
                    "completed": False,
                    "critical": True
                },
                {
                    "checkbox_id": "signout_3",
                    "task": "Swab count verified",
                    "description": "Confirm all sponges and swabs are accounted for",
                    "completed": False,
                    "critical": True
                },
                {
                    "checkbox_id": "signout_4",
                    "task": "Drain management",
                    "description": "Document any drains placed and their location",
                    "completed": False,
                    "critical": False
                },
                {
                    "checkbox_id": "signout_5",
                    "task": "Dressing applied",
                    "description": "Confirm appropriate dressing applied to incision",
                    "completed": False,
                    "critical": False
                }
            ]
        }
    ]
    
    # Calculate completion stats
    total_items = sum(len(cat["items"]) for cat in checklist_items)
    completed_items = sum(
        1 for cat in checklist_items 
        for item in cat["items"] 
        if item.get("completed", False)
    )
    critical_items = sum(
        1 for cat in checklist_items 
        for item in cat["items"] 
        if item.get("critical", False)
    )
    critical_completed = sum(
        1 for cat in checklist_items 
        for item in cat["items"] 
        if item.get("critical", False) and item.get("completed", False)
    )
    
    return {
        "success": True,
        "patient_id": patient_id,
        "procedure": procedure or "General Surgery",
        "checklist": checklist_items,
        "statistics": {
            "total_items": total_items,
            "completed_items": completed_items,
            "completion_percentage": int((completed_items / total_items * 100) if total_items > 0 else 0),
            "critical_items": critical_items,
            "critical_completed": critical_completed,
            "all_critical_complete": critical_completed == critical_items
        },
        "is_ready_for_surgery": critical_completed == critical_items
    }


def validate_checklist_completion(checklist_items: list) -> dict:
    """
    Validate if critical checklist items are completed.
    
    Args:
        checklist_items: List of checklist items with completion status
    
    Returns:
        dict with validation results
    """
    critical_incomplete = [
        item for item in checklist_items
        if item.get("critical", False) and not item.get("completed", False)
    ]
    
    return {
        "success": True,
        "all_critical_complete": len(critical_incomplete) == 0,
        "incomplete_critical_items": [item.get("task", "Unknown") for item in critical_incomplete],
        "can_proceed": len(critical_incomplete) == 0
    }
