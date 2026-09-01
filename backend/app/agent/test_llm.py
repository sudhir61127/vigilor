from backend.app.agent.llm import llm

response = llm.invoke(
    "Say hello to the VIGIL-OR team in one short sentence."
)

print(response.content)