"""
LangGraph workflow for VIGIL-OR agent.
Orchestrates patient queries, medical report retrieval, monitoring, and surgical checklists.
"""

import json
from typing import Any, Dict, Optional
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

# Import tools
from app.tools.rag_tool import search_medical_reports, get_patient_report
from app.tools.patient_tool import search_patient, get_patient_report_list, list_all_patients
from app.tools.checklist_tool import get_surgical_checklist
from app.tools.monitor_tool import get_current_vitals, get_vitals_summary, check_vital_thresholds


class AgentState(BaseModel):
    """State for the agent workflow."""
    user_input: str
    intent: str = ""
    response: str = ""
    context: Dict[str, Any] = Field(default_factory=dict)
    tool_results: Dict[str, Any] = Field(default_factory=dict)


def classify_intent(state: AgentState) -> AgentState:
    """
    Classify the user's intent to determine which tool to use.
    """
    user_input_lower = state.user_input.lower()
    
    # Determine intent based on keywords
    if any(keyword in user_input_lower for keyword in ["checklist", "surgical", "before surgery"]):
        state.intent = "surgical_checklist"
    elif any(keyword in user_input_lower for keyword in ["vitals", "monitor", "heart rate", "spo2", "blood pressure", "temperature", "respiratory"]):
        state.intent = "monitor"
    elif any(keyword in user_input_lower for keyword in ["report", "mri", "ct", "blood", "xray", "ecg"]):
        state.intent = "medical_report"
    elif any(keyword in user_input_lower for keyword in ["patient", "show", "p00", "pat", "information"]):
        state.intent = "patient_info"
    elif any(keyword in user_input_lower for keyword in ["surgical precautions", "precautions", "safety"]):
        state.intent = "medical_knowledge"
    else:
        state.intent = "general"
    
    return state


def handle_patient_info(state: AgentState) -> AgentState:
    """Handle patient information requests."""
    if state.intent != "patient_info":
        return state
    
    # Extract patient ID from input
    patient_id = extract_patient_id(state.user_input)
    
    if patient_id:
        result = search_patient(patient_id)
        state.tool_results["patient_search"] = result
        
        if result.get("success"):
            patient = result.get("patient", {})
            state.response = f"""
**Patient Information**
- Name: {patient.get('name', 'Unknown')}
- ID: {patient.get('patient_id', 'Unknown')}
- Age: {patient.get('age', 'Unknown')} years
- Gender: {patient.get('gender', 'Unknown')}
- Available Reports: {', '.join(patient.get('available_reports', []))}

Available reports for {patient.get('name', 'this patient')} include blood work, MRI, CT scan, ECG, and X-ray reports.
"""
        else:
            state.response = result.get("error", "Could not retrieve patient information.")
    else:
        # List all patients
        result = list_all_patients()
        state.tool_results["patients_list"] = result
        
        if result.get("success"):
            patients = result.get("patients", [])
            patients_str = "\n".join([f"- {p.get('name', 'Unknown')} (ID: {p.get('id', 'Unknown')}, Age: {p.get('age', 'Unknown')})" for p in patients])
            state.response = f"""**Available Patients in the System:**
{patients_str}

Total patients: {result.get('total', 0)}
"""
        else:
            state.response = "Could not retrieve patient list."
    
    return state


def handle_medical_report(state: AgentState) -> AgentState:
    """Handle medical report retrieval."""
    if state.intent != "medical_report":
        return state
    
    # Extract patient ID and report type
    patient_id = extract_patient_id(state.user_input)
    report_type = extract_report_type(state.user_input)
    
    if patient_id and report_type:
        result = get_patient_report(patient_id, report_type)
        state.tool_results["medical_report"] = result
        
        if result.get("success"):
            content = result.get("content", "")
            # Truncate long reports for readability
            if len(content) > 1000:
                content = content[:1000] + "\n\n[Report truncated for display]"
            state.response = f"""**{report_type.upper()} Report - Patient {patient_id}**

{content}
"""
        else:
            state.response = result.get("error", "Could not retrieve report.")
    else:
        # Try general search
        result = search_medical_reports(state.user_input, top_k=2)
        state.tool_results["medical_search"] = result
        
        if result.get("success"):
            results = result.get("results", [])
            response_text = "**Medical Reports Found:**\n"
            for i, res in enumerate(results, 1):
                response_text += f"\n{i}. {res.get('report_type', 'Unknown').upper()} - Patient {res.get('patient_id', 'Unknown')}\n"
                response_text += f"   {res.get('content_preview', '')}\n"
            state.response = response_text
        else:
            state.response = result.get("error", "Could not find relevant medical reports.")
    
    return state


def handle_monitor(state: AgentState) -> AgentState:
    """Handle vital signs monitoring."""
    if state.intent != "monitor":
        return state
    
    # Get current vitals
    result = get_vitals_summary()
    state.tool_results["monitor"] = result
    
    if result.get("success"):
        vitals = result.get("vitals_summary", {})
        
        response_text = "**Current Vital Signs (Simulated Demo Data)**\n\n"
        response_text += "| Vital | Value | Status |\n"
        response_text += "|-------|-------|--------|\n"
        
        for vital_name, vital_data in vitals.items():
            value = vital_data.get("value", "N/A")
            unit = vital_data.get("unit", "")
            status = vital_data.get("status", "unknown").upper()
            vital_display = vital_name.replace("_", " ").title()
            response_text += f"| {vital_display} | {value} {unit} | {status} |\n"
        
        response_text += f"\n*Note: {result.get('note', '')}*"
        
        # Check for warnings
        warning_result = check_vital_thresholds()
        if warning_result.get("has_warnings"):
            warnings = warning_result.get("warnings", [])
            response_text += "\n\n⚠️ **Warnings:**\n"
            for warning in warnings:
                response_text += f"- {warning.get('vital', 'Unknown').replace('_', ' ').title()}: {warning.get('value')} {warning.get('unit', '')}\n"
        
        state.response = response_text
    else:
        state.response = result.get("error", "Could not retrieve vital signs.")
    
    return state


def handle_surgical_checklist(state: AgentState) -> AgentState:
    """Handle surgical checklist requests."""
    if state.intent != "surgical_checklist":
        return state
    
    # Extract patient ID if available
    patient_id = extract_patient_id(state.user_input)
    
    result = get_surgical_checklist(patient_id=patient_id, procedure="General Surgery")
    state.tool_results["checklist"] = result
    
    if result.get("success"):
        stats = result.get("statistics", {})
        checklist = result.get("checklist", [])
        
        response_text = f"""**Surgical Safety Checklist**
Patient: {result.get('patient_id', 'TBD')}
Procedure: {result.get('procedure', 'General Surgery')}

**Status:** {stats.get('completion_percentage', 0)}% Complete ({stats.get('completed_items', 0)}/{stats.get('total_items', 0)} items)
**Critical Items:** {stats.get('critical_completed', 0)}/{stats.get('critical_items', 0)} ✓
**Ready for Surgery:** {'✅ YES' if stats.get('all_critical_complete', False) else '❌ NO - Missing critical verifications'}

"""
        
        # Add checklist categories
        for category in checklist:
            response_text += f"\n**{category.get('category', 'Unknown')}**\n"
            for item in category.get("items", []):
                check = "☑️" if item.get("completed", False) else "☐"
                critical = "⚠️ " if item.get("critical", False) else ""
                response_text += f"  {check} {critical}{item.get('task', 'Unknown')}\n"
        
        state.response = response_text
    else:
        state.response = "Could not generate surgical checklist."
    
    return state


def handle_medical_knowledge(state: AgentState) -> AgentState:
    """Handle medical knowledge queries."""
    if state.intent != "medical_knowledge":
        return state
    
    # Search medical reports for relevant information
    result = search_medical_reports(state.user_input, top_k=3)
    state.tool_results["knowledge_search"] = result
    
    if result.get("success"):
        results = result.get("results", [])
        
        response_text = "**Medical Information from Patient Records:**\n\n"
        
        for i, res in enumerate(results, 1):
            response_text += f"{i}. **{res.get('report_type', 'Unknown').upper()}** from Patient {res.get('patient_id', 'Unknown')}\n"
            response_text += f"   {res.get('content_preview', '')}\n\n"
        
        response_text += "*This information is based on medical reports in the system and is for reference during surgical planning.*"
        
        state.response = response_text
    else:
        # Provide generic surgical safety response
        state.response = """**General Surgical Precautions:**

1. **Patient Identification**: Verify patient identity using two identifiers
2. **Site Marking**: Ensure surgical site is marked with indelible marker
3. **Consent**: Confirm written surgical consent is obtained
4. **NPO Status**: Verify patient fasted appropriately
5. **Allergies**: Confirm all allergies documented and communicated
6. **Imaging**: Ensure all required imaging is available in OR
7. **Equipment**: Verify all surgical instruments and equipment are functional
8. **Counts**: Ensure instrument, sponge, and sharps counts before and after
9. **Timing**: Consider antibiotic prophylaxis timing
10. **Communication**: Ensure clear communication among surgical team members

Always refer to the institutional surgical safety protocol and checklist before proceeding.
"""
    
    return state


def handle_general(state: AgentState) -> AgentState:
    """Handle general queries."""
    if state.intent != "general":
        return state
    
    response_text = """**VIGIL-OR Medical Assistant**

I can help you with:
- **Patient Information**: Ask about a specific patient (e.g., "Show patient P001")
- **Medical Reports**: Retrieve specific reports (e.g., "Show MRI report for P001")
- **Vital Signs**: Check current monitor readings (e.g., "Show current vitals")
- **Surgical Checklist**: Generate pre-surgery checklist (e.g., "Show surgical checklist")
- **Medical Knowledge**: Search medical records (e.g., "What are the surgical precautions?")

How can I assist you in the operating room today?
"""
    
    state.response = response_text
    return state


def create_agent_graph():
    """Create the LangGraph workflow."""
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("handle_patient_info", handle_patient_info)
    workflow.add_node("handle_medical_report", handle_medical_report)
    workflow.add_node("handle_monitor", handle_monitor)
    workflow.add_node("handle_surgical_checklist", handle_surgical_checklist)
    workflow.add_node("handle_medical_knowledge", handle_medical_knowledge)
    workflow.add_node("handle_general", handle_general)
    
    # Add edges
    workflow.add_edge(START, "classify_intent")
    
    workflow.add_conditional_edges(
        "classify_intent",
        lambda state: state.intent,
        {
            "patient_info": "handle_patient_info",
            "medical_report": "handle_medical_report",
            "monitor": "handle_monitor",
            "surgical_checklist": "handle_surgical_checklist",
            "medical_knowledge": "handle_medical_knowledge",
            "general": "handle_general",
        }
    )
    
    # All handlers lead to END
    workflow.add_edge("handle_patient_info", END)
    workflow.add_edge("handle_medical_report", END)
    workflow.add_edge("handle_monitor", END)
    workflow.add_edge("handle_surgical_checklist", END)
    workflow.add_edge("handle_medical_knowledge", END)
    workflow.add_edge("handle_general", END)
    
    return workflow.compile()


def extract_patient_id(text: str) -> Optional[str]:
    """Extract patient ID from text."""
    text_upper = text.upper()
    
    # Look for patterns like P001, PAT001, PAT-001, P00, etc.
    import re
    
    # Try to find PAT/P followed by digits
    match = re.search(r'\b(?:PAT[- ]?)?(?:00)?(\d{1,3})\b', text_upper)
    if match:
        num = match.group(1)
        # Pad to 3 digits
        num = num.zfill(3)
        return f"PAT{num}"
    
    return None


def extract_report_type(text: str) -> Optional[str]:
    """Extract report type from text."""
    text_lower = text.lower()
    
    report_types = ["blood", "mri", "ct", "xray", "x-ray", "ecg", "ekg"]
    
    for report_type in report_types:
        if report_type in text_lower:
            # Normalize the report type
            if report_type == "x-ray":
                return "xray"
            elif report_type in ["ekg", "ecg"]:
                return "ecg"
            return report_type
    
    return None


# Compile the graph
agent_graph = create_agent_graph()


def run_agent(user_input: str) -> Dict[str, str]:
    """
    Run the agent with user input.
    
    Args:
        user_input: The user's query
    
    Returns:
        Dictionary with intent and response
    """
    state = AgentState(user_input=user_input)
    
    try:
        result = agent_graph.invoke(state)
        
        return {
            "intent": result.get("intent", "unknown"),
            "response": result.get("response", "No response generated")
        }
    except Exception as e:
        return {
            "intent": "error",
            "response": f"Error processing request: {str(e)}"
        }
