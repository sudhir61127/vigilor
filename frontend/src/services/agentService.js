const API_BASE_URL = "http://127.0.0.1:8000";

export async function sendToAgent(userInput) {
  const response = await fetch(`${API_BASE_URL}/agent`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_input: userInput,
    }),
  });

  if (!response.ok) {
    throw new Error(`Agent request failed: ${response.status}`);
  }

  return response.json();
}