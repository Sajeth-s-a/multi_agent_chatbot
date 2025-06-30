from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from common.llm_client import claude_client

# Initialize the FastAPI application for this agent service
app = FastAPI(title="Basic Agent Service", version="0.1.0")

# Define a Pydantic model for our incoming request payload
class AgentRequest(BaseModel):
    user_query: str
    session_id: str
    user_id: str
    # We'll add more context fields later

# Define a Pydantic model for our outgoing response payload
class AgentResponse(BaseModel):
    response_text: str
    agent_name: str = "BasicAgent"
    # We'll add more context/metadata fields later

@app.post("/agent/process_query", response_model=AgentResponse)
async def process_agent_query(request: AgentRequest):
    """
    Endpoint for a basic agent to process a user query using Claude.
    """
    print(f"Received query for session {request.session_id}: {request.user_query}")

    try:
        # A simple system message to define the agent's persona
        system_message = "You are a helpful AI assistant. Respond concisely and accurately."

        # Get completion from Claude
        llm_response = await claude_client.get_completion(
            user_message=request.user_query,
            system_message=system_message
        )

        return AgentResponse(response_text=llm_response)
    except Exception as e:
        print(f"Error in agent processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Example of how to run this service (for development)
# You would typically run this using uvicorn from the command line:
# uvicorn agent_service.main:app --reload --port 8001