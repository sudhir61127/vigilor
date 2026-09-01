"""
API routes for VIGIL-OR agent and monitor endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.graph.workflow import run_agent
from app.monitor.monitor import get_monitor_vitals

router = APIRouter()


class AgentRequest(BaseModel):
    """Request model for /agent endpoint."""
    user_input: str


class AgentResponse(BaseModel):
    """Response model for /agent endpoint."""
    intent: str
    response: str


class MonitorResponse(BaseModel):
    """Response model for /monitor endpoint."""
    simulated: bool
    timestamp: str


@router.post("/agent", response_model=AgentResponse)
async def agent_endpoint(request: AgentRequest) -> AgentResponse:
    """
    Process user input through the VIGIL-OR agent.
    
    Request:
        {
            "user_input": "Show patient P001"
        }
    
    Response:
        {
            "intent": "patient_info",
            "response": "Patient information..."
        }
    """
    if not request.user_input or not request.user_input.strip():
        raise HTTPException(status_code=400, detail="user_input cannot be empty")
    
    result = run_agent(request.user_input)
    
    return AgentResponse(
        intent=result.get("intent", "unknown"),
        response=result.get("response", "No response generated")
    )


@router.get("/monitor")
async def monitor_endpoint():
    """
    Get current vital signs from the simulated OR monitor.
    
    Response includes:
        - simulated: true (indicating demo data)
        - timestamp: ISO format timestamp
        - vitals: vital signs with values, units, and status
        - ecg: ECG waveform data
        - note: disclaimer about demo data
    """
    try:
        vitals = get_monitor_vitals()
        return vitals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve vitals: {str(e)}")
