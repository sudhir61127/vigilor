from fastapi import FastAPI
from pydantic import BaseModel

from backend.app.graph.workflow import agent_graph


app = FastAPI(title="VIGIL-OR AI Backend")


class AgentRequest(BaseModel):
    user_input: str


@app.get("/")
def root():
    return {"message": "VIGIL-OR AI Backend is running"}


@app.post("/agent")
def run_agent(request: AgentRequest):
    result = agent_graph.invoke({
        "user_input": request.user_input,
        "intent": "",
        "response": "",
    })

    return {
        "intent": result["intent"],
        "response": result["response"],
    }