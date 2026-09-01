from backend.app.graph.workflow import agent_graph

result = agent_graph.invoke({
    "user_input": "Check the current system status",
    "intent": "",
    "response": "",
})

print("Intent:", result["intent"])
print("Response:", result["response"])