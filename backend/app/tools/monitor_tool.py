"""
Monitor Tool for retrieving and managing vital signs data.
"""

from app.monitor.monitor import get_monitor_vitals, reset_monitor


def get_current_vitals() -> dict:
    """
    Get current vital signs from the OR monitor.
    
    Returns:
        dict with all vital signs and ECG data
    """
    try:
        vitals = get_monitor_vitals()
        return {
            "success": True,
            "data": vitals
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve vitals: {str(e)}"
        }


def get_vitals_summary() -> dict:
    """
    Get a summary of current vital signs (without ECG waveform).
    
    Returns:
        dict with vital signs summary
    """
    try:
        vitals = get_monitor_vitals()
        
        summary = {
            "success": True,
            "timestamp": vitals.get("timestamp"),
            "vitals_summary": {
                key: value for key, value in vitals.get("vitals", {}).items()
            },
            "note": vitals.get("note")
        }
        
        return summary
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get vitals summary: {str(e)}"
        }


def check_vital_thresholds() -> dict:
    """
    Check if any vitals are outside normal thresholds.
    
    Returns:
        dict with warning status
    """
    try:
        vitals = get_monitor_vitals()
        vital_dict = vitals.get("vitals", {})
        
        warnings = []
        for vital_name, vital_data in vital_dict.items():
            if vital_data.get("status") == "warning":
                warnings.append({
                    "vital": vital_name,
                    "value": vital_data.get("value"),
                    "unit": vital_data.get("unit")
                })
        
        return {
            "success": True,
            "has_warnings": len(warnings) > 0,
            "warning_count": len(warnings),
            "warnings": warnings
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to check thresholds: {str(e)}"
        }
