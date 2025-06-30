from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from common.llm_client import claude_client
import logging # Import the logging module

# Import and setup our custom logging configuration FIRST
from config.logging_config import setup_logging
setup_logging() # Call the setup function

# Get a logger instance for this specific module
# Using __name__ is a best practice to organize logs by module
logger = logging.getLogger(__name__)

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
    # Use the logger instead of print
    logger.info(f"Received query for session {request.session_id}, user {request.user_id}: '{request.user_query}'")

    try:
        system_message = "You are a helpful AI assistant. Respond concisely and accurately."
        logger.debug(f"Sending message to Claude: User='{request.user_query}', System='{system_message}'")

        llm_response = await claude_client.get_completion(
            user_message=request.user_query,
            system_message=system_message
        )
        
        logger.info(f"Claude responded for session {request.session_id}: '{llm_response[:50]}...'") # Log truncated response
        return AgentResponse(response_text=llm_response)
    except Exception as e:
        logger.error(f"Error in agent processing for session {request.session_id}: {e}", exc_info=True) # Log full exception info
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# Example of how to run this service (for development)
# uvicorn agent_service.main:app --reload --port 8001