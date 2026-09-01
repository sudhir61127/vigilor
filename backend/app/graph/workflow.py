import re
from typing import TypedDict

from langgraph.graph import StateGraph, END

from backend.app.agent.llm import llm
from backend.app.tools.patient_tool import get_patient
from backend.app.tools.rag_tool import search_medical_documents
from backend.app.tools.monitor_tool import get_monitor_status
from backend.app.tools.checklist_tool import get_checklist


class AgentState(TypedDict):
    user_input: str
    intent: str
    response: str
    tool_result: dict


def understand_intent(state: AgentState):

    user_input = state["user_input"].lower()

    if "patient" in user_input or "patient id" in user_input:
        intent = "patient"

    elif any(word in user_input for word in [
        "monitor",
        "vital",
        "heart rate",
        "blood pressure",
        "spo2",
        "oxygen"
    ]):
        intent = "monitoring"

    elif any(word in user_input for word in [
        "checklist",
        "check list",
        "safety checks"
    ]):
        intent = "checklist"

    elif any(word in user_input for word in [
        "precaution",
        "complication",
        "contraindication",
        "guideline",
        "medical",
        "treatment",
        "surgical"
    ]):
        intent = "rag"

    else:
        intent = "general"

    return {
        "intent": intent
    }

def route_intent(state: AgentState):
    intent = state["intent"]

    if intent == "patient":
        return "patient_tool"

    if intent == "rag":
        return "rag_tool"

    if intent == "monitoring":
        return "monitor_tool"

    if intent == "checklist":
        return "checklist_tool"

    return "generate_response"


def run_patient_tool(state: AgentState):
    user_input = state["user_input"]

    match = re.search(r"\bP\d+\b", user_input.upper())

    if not match:
        return {
            "tool_result": {
                "error": "No patient ID found. Please provide a patient ID such as P001."
            }
        }

    patient_id = match.group(0)

    result = get_patient(patient_id)

    return {
        "tool_result": result
    }


def run_rag_tool(state: AgentState):
    result = search_medical_documents(state["user_input"])

    return {
        "tool_result": result
    }


def run_monitor_tool(state: AgentState):
    result = get_monitor_status()

    return {
        "tool_result": result
    }


def run_checklist_tool(state: AgentState):
    result = get_checklist()

    return {
        "tool_result": result
    }


def generate_response(state: AgentState):

    intent = state["intent"]
    tool_result = state.get("tool_result", {})

    if intent == "patient":
        return {
            "response": f"Here are the patient details:\n{tool_result}"
        }

    if intent == "rag":
        return {
            "response": f"Here is the relevant medical information:\n{tool_result}"
        }

    if intent == "monitoring":
        return {
            "response": f"Current monitor status:\n{tool_result}"
        }

    if intent == "checklist":
        return {
            "response": f"Here is the surgical checklist:\n{tool_result}"
        }

    return {
        "response": "Hello! I am the VIGIL-OR surgical assistant. How can I help?"
    }


def build_agent_graph():

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("understand_intent", understand_intent)
    graph.add_node("patient_tool", run_patient_tool)
    graph.add_node("rag_tool", run_rag_tool)
    graph.add_node("monitor_tool", run_monitor_tool)
    graph.add_node("checklist_tool", run_checklist_tool)
    graph.add_node("generate_response", generate_response)

    # Starting point
    graph.set_entry_point("understand_intent")

    # Intent routing
    graph.add_conditional_edges(
        "understand_intent",
        route_intent,
        {
            "patient_tool": "patient_tool",
            "rag_tool": "rag_tool",
            "monitor_tool": "monitor_tool",
            "checklist_tool": "checklist_tool",
            "generate_response": "generate_response",
        },
    )

    # Tool → response
    graph.add_edge("patient_tool", "generate_response")
    graph.add_edge("rag_tool", "generate_response")
    graph.add_edge("monitor_tool", "generate_response")
    graph.add_edge("checklist_tool", "generate_response")

    # Response → end
    graph.add_edge("generate_response", END)

    return graph.compile()


agent_graph = build_agent_graph()